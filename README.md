# Running Locally

## Prerequisites

### Docker

This app is setup with docker-compose so that you can run things locally without needing to install anything other than [Docker](https://docs.docker.com/get-docker/). Install that if you don't have it already.

### .env File

The docker-compose file relies on several environment variables to be set to run properly. Supply these variables using a [".env" file](https://docs.docker.com/compose/env-file/). Simply create a file called `.env` at the root of the project and copy the following contents into it:

```
AWS_ACCESS_KEY_ID=fakeAccessKey
AWS_SECRET_ACCESS_KEY=fakeSecretAccessKey
FLASK_ENV=development
UI_LOCALHOST_PORT=3000
API_LOCALHOST_PORT=5000
```

## Run It

Once the above prerequistes have been satisfied we're ready to let Docker Compose do it's magic. Simply run the following command from the root of the project.

```sh
docker-compose up
```
