mkdir -m 700 .sec
tsig-keygen pydnsapi-bind9  > ./.sec/pydnsapi-bind9.key
TSIG_PASSWORD=$(grep secret .sec/pydnsapi-bind9.key |  cut -f2 -d \")
pydns_api_key=$(dd if=/dev/urandom bs=64 count=1 status=none | base64)
echo "$pydns_api_key" > ./apikeys.pass
chmod 600 apikeys.pass
cp ./.sec/pydnsapi-bind9.key ./config/bind9/

echo "BIND_SERVER=172.25.0.20" > ./.env 
echo "TSIG_USERNAME=pydnsapi-bind9" >> ./.env 
echo TSIG_PASSWORD=${TSIG_PASSWORD} >> ./.env 
echo "BIND_ALLOWED_ZONES=example.com,example.org" >> ./.env
echo "API_KEY_FILE=apikeys.pass" >> ./.env
echo "LOGGING_APPLICATION_NAME=pydns-api-ddev" >> ./.env
echo "LOGGING_DIR=./logs" >> ./.env

