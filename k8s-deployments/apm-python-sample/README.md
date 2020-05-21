# Sample Flask App Docker Container 

* Build

```
docker build -t apm-python-sample:latest .
```

* Test 

```
docker run -d -p 5050:5050 apm-python-sample:latest
curl http://localhost:5050
```

* Push

``` 
docker login --username=yourhubusername
docker images
docker tag apm-python-sample:latest yourhubusername/apm-python-sample:latest
docker push yourhubusername/apm-python-sample:latest
docker logout
```

