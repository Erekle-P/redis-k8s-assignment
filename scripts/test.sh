#!/bin/bash
set -e

read -p "Enter the key: " key
read -p "Enter the value: " value

base_url="http://localhost/api"

curl -X POST "${base_url}/cache?key=${key}&value=${value}"
echo
curl "${base_url}/cache?key=${key}"
echo
