#!/bin/bash

export HOME=/opt/bindapi

# Pyenv
export PATH="/opt/bindapi/venvapi/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

source $HOME/venv/pyenv.cfg

pyenv activate venvapi

cd $HOME/venvapi
uvicorn bindapi:app

