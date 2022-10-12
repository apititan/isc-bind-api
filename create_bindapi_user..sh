#!/bin/bash
sudo useradd -r -m -d /opt/pydnsapi pydnsapi -s /bin/bash
sudo su - pydnsapi
mkdir venvapi
python3 -m venv venvapi
ls -al venvapi
