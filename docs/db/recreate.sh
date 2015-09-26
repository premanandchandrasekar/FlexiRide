#! /bin/bash

psql -U postgres -d postgres -f dbUser.sql
psql -U postgres -d postgres -c "DROP DATABASE flexiride;"
psql -U postgres -d postgres -c "CREATE DATABASE flexiride WITH owner=foo ENCODING='utf-8';"
psql -U postgres -d flexiride -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'

psql -U foo -d flexiride -f schema.sql
