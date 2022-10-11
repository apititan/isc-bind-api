## Building pydnsapi Docker Image

Executing the following comman to build the docker image locally

```
docker build -t apititan/pydnsapi .
```

## Image-building best practices

### Security scanning

Using the ```docker scan``` command to check an image for security flaws after it has been created is a recommended practice. 
Snyk and Docker have teamed up to offer the vulnerability scanning service.

***Note:**

You must have a docker hub login account in order to use this service. 
Create one at [hub.docker.com](https://hub.docker.com/) if you don't already have one.

To examine the pydnsapi image you previously created, simply type the command below.

```
docker scan pydnsapi
```





