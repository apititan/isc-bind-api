#!/usr/bin/env fish

export (cat config.env)
uvicorn bindapi:app

