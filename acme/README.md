## Leveraging LetsEncrypt to generate SSL certificates

You may use this shell script to issue LetsEncrypt certificates using the ```pydnsapi```.
Visit https://acme.sh for additional details on the acme.sh utility.
Enter the following command in your Linux or MacOS terminal to create a 64-bit secure API 
key that will be used as your ```pydns_api_key```. It creates a key that is 64 bit and based64 encoded.
```
source  ../.env
```
Next, use the following command to export your pydns_api_url. for example.

```
export pydns_api_url="https://pydnsapi.yourdomain.tld" 
```

The following is a full test command for the acme.sh tool.

```
./acme.sh --insecure --issue --staging --debug 2 --domain yourdomain.tld --dns dns_pydnstapi | tee debug_run.log
```

```
Usage: add _acme-challenge.host.yourdomain.tld "XXXXXXXX"
```
