# this usage is an example to write data to influxdb in a server
curl -i -XPOST 'https://sensorweb.us:8086/write?db=testdb' -u test:sensorweb --data-binary 'weather,location=UGA temperature=88 1586651070000000000'
# curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary @cpu_data.txt

# 1586651070000000000
# 1422568543702900257
# Epoch timestamp: 1586651070 + 9 0s
# Timestamp in milliseconds: 1586651070000
# Date and time (GMT): Sunday, April 12, 2020 0:24:30
# Date and time (your time zone): Saturday, April 11, 2020 20:24:30 GMT-04:00

# this usage is an example to read data from influxdb in a server with a given time range in ascii 
curl -G "https://sensorweb.us:8086/query?pretty=true&db=testdb" -u test:sensorweb --data-urlencode "q=SELECT temperature FROM weather WHERE location = 'UGA' AND time >= '2020-04-12 00:24:30.000' and time <= '2020-04-12 00:24:31.000'"

# this usage is an example to read data from influxdb in a server with a specific timestamp in epoch time; epoch time can also be used to specify a range
curl -G "https://sensorweb.us:8086/query?pretty=true&db=testdb" -u test:sensorweb --data-urlencode "q=SELECT temperature FROM weather WHERE location = 'UGA' AND time=1586651070000000000"

curl -G "https://sensorweb.us:8086/query?pretty=true&db=testdb" -u test:sensorweb --data-urlencode "q=SELECT temperature FROM weather WHERE location = 'UGA' AND time>=1586651070000000000 AND time<=1586652070000000000"

# this usage will send data to https server without verifying server certificate
curl -s --insecure POST 'https://sensorweb.local:8086/write?db=algtest' -u test:sensorweb --data-binary 'weather,location=UGA temperature=108 1586651070000000000'

# this usage will send data to https server without verifying server certificate
curl -G --insecure "https://sensorweb.local:8086/query?pretty=true&db=algtest" -u test:sensorweb --data-urlencode "q=SELECT temperature FROM weather WHERE location = 'UGA' AND time=1586651070000000000"
