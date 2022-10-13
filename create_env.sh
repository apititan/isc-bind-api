mkdir -p -m 700 .sec
tsig-keygen pydnsapi-nsapi1  > ./.sec/pydnsapi-nsapi1.key
TSIG_PASSWORD=$(grep secret .sec/pydnsapi-nsapi1.key |  cut -f2 -d \")
pydns_api_pass=$(date | sha256sum | base64 | head -c 64; echo)
echo "pydns_api-key,$pydns_api_pass" > ./apikeys.pass
chmod 600 apikeys.pass
sudo cp ./.sec/pydnsapi-nsapi1.key /etc/bind/pydnsapi-nsapi1.conf

echo "BIND_SERVER=172.25.0.20" > ./.env 
echo "TSIG_USERNAME=pydnsapi-nsapi1" >> ./.env 
echo TSIG_PASSWORD=${TSIG_PASSWORD} >> ./.env 
echo "BIND_ALLOWED_ZONES=example.com,example.org" >> ./.env
echo "API_KEY_FILE=apikeys.pass" >> ./.env
echo "LOGGING_APPLICATION_NAME=pydnsapi-nsapi1" >> ./.env
echo "LOGGING_DIR=./logs" >> ./.env

                  
