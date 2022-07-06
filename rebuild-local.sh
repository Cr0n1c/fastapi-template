#/bin/sh
PWD=$(pwd)

LOCAL_DB_ROOT=$PWD/db
LOCAL_POSTGRES_ROOT=$LOCAL_DB_ROOT/web
LOCAL_NEO4J_ROOT=$LOCAL_DB_ROOT/data

# Ensuring old artifacts are gone
rm -rf $PWD/db

# Creating folder structure
mkdir $LOCAL_DB_ROOT

for LOCAL_DB in $LOCAL_NEO4J_ROOT
do
    mkdir $LOCAL_DB
    mkdir $LOCAL_DB/db $LOCAL_DB/logs $LOCAL_DB/data
done
