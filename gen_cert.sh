#!/bin/bash

# ================================================================
#
# A quick script for generating self signed certificate to "./cert/"
#
# ================================================================

# 2 letter ISO country code
C="US"

# State
ST="CA"

# Location, City
L="LA"

# Organization
O=""

# Organizational Unit, Department
OU=""

# Common Name
CN=""



SUBJ=""
if [ "$C" != "" ]; then
    SUBJ="$SUBJ/C=$C"
fi

if [ "$ST" != "" ]; then
    SUBJ="$SUBJ/ST=$ST"
fi

if [ "$L" != "" ]; then
    SUBJ="$SUBJ/L=$L"
fi

if [ "$O" != "" ]; then
    SUBJ="$SUBJ/O=$O"
fi

if [ "$OU" != "" ]; then
    SUBJ="$SUBJ/OU=$OU"
fi

if [ "$CN" != "" ]; then
    SUBJ="$SUBJ/CN=$CN"
fi



mkdir cert
rm cert/*
cd cert
openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
openssl rsa -passin pass:x -in server.pass.key -out server.key

rm server.pass.key
if [ "$SUBJ" == "" ]; then
    openssl req -new -key server.key -out server.csr
else
    openssl req -new -key server.key -out server.csr -subj "${SUBJ}"
fi

openssl x509 -req -sha256 -days 365 -in server.csr -signkey server.key -out server.crt
