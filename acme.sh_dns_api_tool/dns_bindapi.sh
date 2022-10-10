#!/usr/bin/env sh
# HELP: 
# With this bind API, you can issue letsEncrypt certificates using this shell script.
# For more information on the acme.sh tool, please visit https://acme.sh.
# In your Linux/MacOS terminal, type the following command to generate 
# a 64bit secure API key  to be used as your BIND REST API KEY. 
# It generates a 64bit based64 encoded key.
# Execute: export bindrestapi_key=$(dd if=/dev/urandom bs=64 count=1 status=none | base64) 
# Next, use the following command to export your BIND REST API URL.
# Execute: export bindrestapi_url="https://dnsapi.yourdomain.tld" for example.
# 
# The following is a full test command for the acme.sh tool.
# Execute: ./acme.sh --insecure --issue --staging --debug 2 --domain yourdomain.tld --dns dns_bindrestapi | tee debug_run.log
# Usage: add _acme-challenge.host.yourdomain.tld "XXXXXXXX"

dns_bindrestapi_add() {
  fulldomain=$1
  txtvalue=$2

  if [ "$bindrestapi_key" ]; then
    _saveaccountconf_mutable bindrestapi_key "$bindrestapi_key"
  else
    _err "You did not provide a bindrestapi_key; please review the documentation again."    
    return 1
  fi

  if [ "$bindrestapi_url" ]; then
    _saveaccountconf_mutable bindrestapi_url "$bindrestapi_url"
  else
    _err "You did not provide a bindrestapi url; please review the documentation again."
    return 1

  fi

  _info "Adding record $fulldomain"
  export _H1="X-Api-Key: $bindrestapi_key"
  export _H2="Content-Type: application/json"
  data="{\"response\":\"$txtvalue\",\"rrtype\":\"TXT\",\"ttl\":30}"
  _debug "data: $data"
  response="$(_post "$data" "$bindrestapi_url/dns/record/$fulldomain")"
  _debug "got response: $response"
}

dns_bindrestapi_rm() {
  fulldomain=$1
  txtvalue=$2

  if [ "$bindrestapi_key" ]; then
    _saveaccountconf_mutable bindrestapi_key "$bindrestapi_key"
  else
    _err "You did not provide a bindrestapi_key; please review the documentation again"
    return 1
  fi

  if [ "$bindrestapi_url" ]; then
    _saveaccountconf_mutable bindrestapi_url "$bindrestapi_url"
  else
    _err "You did not provide a bindrestapi url; please review the documentation again  "
    return 1
  fi

  _info "deleting record $fulldomain"
  export _H1="X-Api-Key: $bindrestapi_key"
  export _H2="Content-Type: application/json"
  data="{\"response\":\"$txtvalue\",\"rrtype\":\"TXT\",\"ttl\":30}"
  _debug "data: $data"
  response="$(_post "$data" "$bindrestapi_url/dns/record/$fulldomain" "" "DELETE")"
  _debug "got response: $response"
}
