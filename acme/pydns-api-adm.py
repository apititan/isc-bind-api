#!/usr/bin/env sh

pydnsapi_add() {
  fulldomain=$1
  txtvalue=$2

  if [ "$bkey" ]; then
    _saveaccountconf_mutable pydns_api_key "$pydns_api_key"
  else
    _err "You did not provide a pydns_api_key; please review the documentation again."    
    return 1
  fi

  if [ "$bindrestapi_url" ]; then
    _saveaccountconf_mutable pydns_api_url "$pydapi_url"
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
