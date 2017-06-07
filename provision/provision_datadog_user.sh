#!/bin/bash
echo "db.createUser({
    \"user\":\"$MONGO_DATADOG_USER\",
    \"pwd\": \"$MONGO_DATADOG_PASSWORD\",
    \"roles\" : [
        {role: 'read', db: 'admin' },
        {role: 'clusterMonitor', db: 'admin'},
        {role: 'read', db: 'local'}
    ]
})" | mongo db/admin &&

echo "db.auth('$MONGO_DATADOG_USER', '$MONGO_DATADOG_PASSWORD')" | mongo db/admin | grep -E "(Authentication failed)|(auth fails)" &&
echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"
