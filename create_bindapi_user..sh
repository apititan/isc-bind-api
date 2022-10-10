#!/bin/bash
sudo useradd -r -m -d /opt/bindapi bindapi -s /bin/bash
sudo su - bindapi
mkdir venvapi
python3 -m venv venvapi
ls -al venvapi
