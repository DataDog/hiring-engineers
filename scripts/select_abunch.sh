#!/bin/bash

i="0"
while [ $i -lt 1500 ]; do
        sudo mysql -u datadog --password='datadog' -e 'SELECT * FROM mluptons_schema.mytable'
        i = $[$i+1]
done
