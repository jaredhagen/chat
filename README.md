# Preface

TODO Flesh this out or remove it.

There is way more work here than I initially thought. There is still a ton of work I'd like to do (especially in the UI) but I'm mostly happy with where things are at.

The API is Flask app. I've never worked with Flask before. I stuck pretty closely to the project structure recommend in the offical Flask documentation.

# Running Locally

## Prerequisites

### Docker

This app is setup with docker-compose so that you can run things locally without needing to install anything other than [Docker](https://docs.docker.com/get-docker/). Install that if you don't have it already.

## Run It

We're ready to let Docker Compose do it's magic. Simply run the following command from the root of the project.

Note: The docker-compose.yml is configured using `.env` file at the root of the project. You can change things like what localhost port numbers are used for each of the services there.

Note: Twice I've noticed the `dynamodb-setup` container start up and run before the `dynamodb` container is ready to handle requests. It's rare but, if this happens just run `docker-compose up dynamodb-setup` in another terminal window.

```sh
docker-compose up
```

That command is spinning up the following services:

1. `api` - A Flask app served on http://localhost:5000 by default
1. `ui` - A React app served on http://localhost:3000 by default
1. `dynamodb` - An instance of DynamoDB Local. Table data is persisted as long as this service is running. When the service stops all data in it is lost.
1. `dynamodb-setup` - This service starts up creates the DynamoDB table and then exits.

# Testing

## API Integration Tests

The API has a suite of integration tests that can be run using the following docker command. The services in this docker compose file are stand-alone (i.e. they are not dependent on any other running services and can safely be run without affecting data in other DynamoDB Local instances).

```sh
docker-compose -f docker-compose.tests.yml up --build --abort-on-container-exit
```

## Postman Collection

A [Postman](https://www.postman.com/downloads/) collection is available for interacting with the API. The collection is dependent on a global or environment variable called `chat_username`. Once you've set that you just need to use the Register User request and you're good to go.

# Local Docker Development (In Docker)

I stumbled across the following extension it in the process of working through some Docker things and thought I'd share it. I thought it was cool. The extension allows you to develop in VSCode using the file system of a Docker container. Which allows you to code without having to install any thing on your local machine. There's support for defining a `devcontainer.json` file to create a predefined tool and runtime-stack.

### Extension

https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

### Usage Example

https://code.visualstudio.com/docs/remote/containers

# TODO: Decide if these should be talking points or included in the README.

- API: Unit test should be added in addition to the existing integration tests.
- API: More comprehensive DynamoDB error handling should be put in place.
- API: DynamoDB query pagination could be added to support things like infinite scrolling.
- UI: More comprehensive API error handling should be put in place.
- UI: `react-query` uses some pretty aggresive refetching of stale data these settings could be tuned down.
- UI: The copy in the UI should really be templatized for localization support.
- UI: Accessibility was not really a consideration as I built out the UI. Screen reader landmarks and keyboard controls along with things like color contrast all could all be looked into.
- UI: The UI has no tests. I just ran out of time. My React skills were (and still are) very rusty going into this.
