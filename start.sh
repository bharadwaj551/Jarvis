#!/bin/bash
apt-get update
apt-get install -y espeak-ng
gunicorn main:app
