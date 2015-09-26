#! /bin/bash

psql -U postgres -d postgres -f dbUser.sql
psql -U postgres -d postgres -c "DROP DATABASE paypal;"
psql -U postgres -d postgres -c "CREATE DATABASE paypal WITH owner=foo ENCODING='utf-8';"
psql -U postgres -d paypal -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'

psql -U foo -d paypal -f schema.sql
