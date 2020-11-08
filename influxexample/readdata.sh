# this scrit is an example to read data from influxdb in our server

curl -G "https://sensorweb.us:8086/query?pretty=true&db=testdb" -u test:sensorweb --data-urlencode "q=SELECT value FROM temperature WHERE location = 'UGA' AND time > '2020-04-12 00:24:30.000' and time < '2020-04-12 00:24:31.000'"

