import dns.tsigkeyring
import dns.resolver
import dns.update
import dns.query
import dns.zone
import dns.asyncquery
import dns.asyncresolver
import dns.name
import os
import functools
import traceback
import pathlib
import logging
from typing import Optional, List, Tuple
from enum import Enum
from collections import defaultdict, namedtuple
from fastapi import FastAPI, HTTPException, Security, Depends, Query, Path
from fastapi.security.api_key import APIKey, APIKeyHeader
from pydantic import BaseModel, Field

# Create required global variables.
DNS_SERVER = os.environ['BIND_SERVER']
LOGGING_APPLICATION_NAME = os.environ['LOGGING_APPLICATION_NAME']
LOGGING_DIR = os.environ.get("LOGGING_DIR", "./logs")
TSIG = dns.tsigkeyring.from_text({os.environ['TSIG_USERNAME']: os.environ['TSIG_PASSWORD']})
VALID_ZONES   = [i + '.' for i in os.environ['BIND_ALLOWED_ZONES'].split(',')]
API_KEYS      = {
    x.split(',', maxsplit=1)[1]: x.split(',', maxsplit=1)[0]
    for x in 
    filter(lambda x: x != '' and x[0] != '#', pathlib.Path(os.environ['API_KEY_FILE']).read_text().split('\n'))
}


# Set up the logging process. 
formatter = logging.Formatter(f"%(asctime)s == {LOGGING_APPLICATION_NAME} == %(message)s", datefmt='%Y-%m-%dT%H:%M%z')
auditlogger = logging.getLogger('pydnsapi.audit')
auditlogger.setLevel(logging.INFO)
handler1 = logging.handlers.TimedRotatingFileHandler(f'{LOGGING_DIR}/pydnsapi-audit.log', when='D', interval=7)
handler1.setFormatter(formatter)
auditlogger.addHandler(handler1)
logger = logging.getLogger('pydnsapi')
logger.setLevel(logging.DEBUG)
handler2 = logging.handlers.RotatingFileHandler(f'{LOGGING_DIR}/pydnsapi-debug.log', maxBytes=(1024 * 1024 * 100), backupCount=10)
handler2.setFormatter(formatter)
logger.addHandler(handler2)
logger.debug('Starting up')

# Record types that can be used for CRUD operations.
class RecordType(str, Enum):
    a = 'A'
    aaaa = 'AAAA'
    cname = 'CNAME'
    mx = 'MX'
    ns = 'NS'
    txt = 'TXT'
    soa = 'SOA'
    ptr = 'PTR'

# Record
class Record(BaseModel):
    response: str = Field(..., example='172.25.0.10')
    rrtype: RecordType
    ttl: int = Field(3600, example=3600)

HelperResponse = namedtuple('HelperResponse', 'domain action zone')

# Some wrappers
asyncresolver = dns.asyncresolver.Resolver()
asyncresolver.nameservers = [DNS_SERVER]
tcpquery = functools.partial(dns.asyncquery.tcp, where=DNS_SERVER)
# used to correct unqualified domains properly
qualify = lambda s: f'{s}.' if not s.endswith('.') else s

# Set up the  app
app = FastAPI(title='pydnsapi', version='v1.0.0')


# Set up API Key authorization
async def check_api_key(api_key_header: str = Security(APIKeyHeader(name='X-Api-Key'))) -> str:
    try:
        return API_KEYS[api_key_header]
    except KeyError:
        raise HTTPException(401, 'invalid api key')


@app.get('/dns/zone/{zone_name}')
def get_zone(zone_name: str = Path(..., example='example.org.'), api_key_name: APIKey = Depends(check_api_key)):
    '''To read (or retrieve) a representation of a resource, use the HTTP GET method. 
       GET returns a representation in JSON and an HTTP response status code of 200 
       in the event of success (or non-error) (OK). In our scenario, we receive a 
       JSON dump of the whole ZONE configuration file.
    axfr
    '''
    logger.debug(f'api key {api_key_name} requested zone {zone_name}')

    zone_name = qualify(zone_name)

    if zone_name not in VALID_ZONES:
        raise HTTPException(400, 'zone file is not allowed')
    
    zone = dns.zone.from_xfr(dns.query.xfr(DNS_SERVER, zone_name))
    
    result = {}
    records = defaultdict(list)
    for (name, ttl, rdata) in zone.iterate_rdatas():
        if rdata.rdtype.name == 'SOA':
            result['SOA'] = {
                'ttl': ttl,
            }
            for n in ('expire', 'minimum','refresh','retry','rname','mname','serial'):
                if n in ('rname', 'mname'):
                    result['SOA'][n] = str(getattr(rdata, n))
                else:
                    result['SOA'][n] = getattr(rdata, n)
        else:
            records[str(name)].append({
                'response': str(rdata),
                'rrtype': rdata.rdtype.name,
                'ttl': ttl,
            })
    result['records'] = records
    logger.debug(f'api key {api_key_name} requested zone {zone_name} - sending zone')
    return result


@app.get('/dns/record/{domain}')
async def get_record(domain: str = Path(..., example='server.example.org.'), record_type: List[RecordType] = Query(list(RecordType)), api_key_name: APIKey = Depends(check_api_key)):
    domain = qualify(domain)
    logger.debug(f'api key {api_key_name} requested domain records {domain} with types {record_type}')

    if not domain.endswith(tuple(VALID_ZONES)):
        raise HTTPException(400, 'domain is not permitted')
    
    records = defaultdict(list)
    for t in record_type:
        try:
            answers = await asyncresolver.resolve(domain, t)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            continue
        records[t] = [str(x) for x in answers.rrset]
    
    return records
        

async def dns_update_helper(domain: str = Path(..., example='server.example.org.')):
    domain = qualify(domain)

    for valid_zone in VALID_ZONES:
        if domain.endswith(valid_zone):
            action = dns.update.Update(valid_zone, keyring=TSIG)
            return HelperResponse(domain=domain, action=action, zone=valid_zone)
    raise HTTPException(400, 'domain zone is not permitted')


@app.post('/dns/record/{domain}')
async def create_record(
            record: Record,
            helper: HelperResponse = Depends(dns_update_helper),
            api_key_name: APIKey = Depends(check_api_key),
        ):
    try:
        helper.action.add(dns.name.from_text(helper.domain), record.ttl, record.rrtype, record.response)
        try:
            await tcpquery(helper.action)
        except Exception:
            logger.debug(traceback.format_exc())
            raise HTTPException(500, 'Failure of a DNS transaction; please check logs')

        auditlogger.info(f'CREATE {helper.domain} {record.rrtype} {api_key_name} -> {helper.domain} record {record} for key {api_key_name}')
    except:
        auditlogger.error(f'FAILED:CREATE {helper.domain} {record.rrtype} {api_key_name} -> {helper.domain} record {record} for key {api_key_name}')
        raise


@app.put('/dns/record/{domain}')
async def replace_record(
            record: Record,
            helper: HelperResponse = Depends(dns_update_helper),
            api_key_name: APIKey = Depends(check_api_key),
        ):
    try:
        helper.action.replace(dns.name.from_text(helper.domain), record.ttl, record.rrtype, record.response)
        try:
            await tcpquery(helper.action)
        except Exception:
            logger.debug(traceback.format_exc())
            raise HTTPException(500, 'DNS transaction failed - check logs')
        auditlogger.info(f'REPLACE {helper.domain} {record.rrtype} {api_key_name} -> {helper.domain} record {record} for key {api_key_name}')
    except:
        auditlogger.info(f'FAILED:REPLACE {helper.domain} {record.rrtype} {api_key_name} -> {helper.domain} record {record} for key {api_key_name}')
        raise


@app.delete('/dns/record/{domain}')
async def delete_single_record(
            record: Record,
            helper: HelperResponse = Depends(dns_update_helper),
            api_key_name: APIKey = Depends(check_api_key),
        ):
    try:
        helper.action.delete(dns.name.from_text(helper.domain), record.rrtype, record.response)
        try:
            await tcpquery(helper.action)
        except Exception:
            logger.debug(traceback.format_exc())
            raise HTTPException(500, 'DNS transaction failed; please review logs')
        auditlogger.info(f'DELETE {helper.domain} {record.rrtype} {api_key_name} -> {helper.domain} record {record} for key {api_key_name}')
    except:
        auditlogger.info(f'FAILED:DELETE {helper.domain} {record.rrtype} {api_key_name} -> {helper.domain} record {record} for key {api_key_name}')
        raise


@app.delete('/dns/allrecords/{domain}')
async def delete_record_type(
            recordtypes: List[RecordType] = Query(list(RecordType)),
            helper: HelperResponse = Depends(dns_update_helper),
            api_key_name: APIKey = Depends(check_api_key),
        ):
    try:
        for rtype in recordtypes:
            logger.debug(f'deleteing {helper.domain} type {rtype}')
            helper.action.delete(dns.name.from_text(helper.domain), rtype)
            try:
                await tcpquery(helper.action)
            except Exception:
                logger.debug(traceback.format_exc())
                raise HTTPException(500, 'DNS transaction failed; please review logs.')
        auditlogger.info(f'DELETE {helper.domain} {",".join(recordtypes)} {api_key_name} -> {helper.domain} record {recordtypes} for key {api_key_name}')
    except:
        auditlogger.info(f'FAILED:DELETE {helper.domain} {",".join(recordtypes)} {api_key_name} -> {helper.domain} record {recordtypes} for key {api_key_name}')
        raise        
        
