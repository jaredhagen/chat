# Chat

## Overview

The repo has two projects in it. An API found in `/app` and a UI found in `/ui`.

### API

The API is a [Flask](https://flask.palletsprojects.com/en/1.1.x/) app. The project structure of the API follows the project structure outlined in the Flask documentation [here](https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/). The API is backed by [DynamoDB](https://aws.amazon.com/dynamodb/) for data storage.

### UI

The UI is a React app. The files in the UI are grouped by type (components, hooks, pages). The UI is built using the [Ant Design](https://ant.design/) component library and uses [react-query](https://react-query.tanstack.com/) for fetching, caching, synchronizing and updating server state.

## Running Locally

The project is setup with [docker-compose](https://docs.docker.com/compose/) so that you can run things locally without needing to install anything other than [Docker](https://docs.docker.com/get-docker/). Install that if you don't have it already. Then run the following command from the root of the project:

**Note: Twice I've noticed the `dynamodb-setup` container start up and run before the `dynamodb` container is ready to handle requests. It's rare but, if this happens just run `docker-compose up dynamodb-setup` in another terminal window.**

```sh
docker-compose up
```

That command is spinning up the following services:

1. `api` - A Flask app served on http://localhost:5000 by default
1. `ui` - A React app served on http://localhost:3000 by default
1. `dynamodb` - An instance of DynamoDB Local. Table data is persisted as long as this service is running. When the service stops all data in it is lost.
1. `dynamodb-setup` - This service starts up creates the DynamoDB table and then exits.

## Configuration

The docker-compose.yml is configured using `.env` file at the root of the project. You can change things like what localhost port numbers are used for each of the services there.

**Note: If you change the localhost ports, the console ouput from the containers will not reflect those changes because the the port definitions only change the local port mapping in the docker compose file.**

## Testing

### API Integration Tests

The API has a suite of integration tests that can be run using the following docker command. The services in this docker compose file are stand-alone (i.e. they are not dependent on any other running services and can safely be run without affecting data in other DynamoDB Local instances).

```sh
docker-compose -f docker-compose.tests.yml up --build --abort-on-container-exit
```

### Postman Collection

A [Postman](https://www.postman.com/downloads/) collection is available for interacting with the API. The collection is dependent on a global or environment variable called `chat_username`. Once you've set that you just need to use the Register User request and you're good to go.

## Local Development

### API

1. Starting from the `/api` folder. Follow the steps [here](https://flask.palletsprojects.com/en/1.1.x/installation/#create-an-environment) for creating and activating a virtual environment.
1. Install project requirements: `pip install -r requirements.txt`
1. Run the api and dynamodb services using `docker-compose up api dynamodb dynamodb-setup`
1. Write some code. Local files are synced with docker using volumes which will trigger
   auto reloading.

- The following commands can be used for automatic formatting and linting
  - Automatic formatting: `python -m black .`
  - Linting: `python -m pylint chat_app`

### UI

1. Starting from the `/ui` folder. Install node_modules using `yarn install`
1. Run the ui and backend services using `docker-compose up`
1. Write some code. Local files are synced with docker using volumes which will trigger
   auto reloading.

- The following command can be used for automatic formatting and linting
  - `yarn run lint`

## TODO

- Workflow: Setup containerized development environment. [Start here.](https://docs.microsoft.com/en-us/learn/modules/use-docker-container-dev-env-vs-code/)
- Workflow: Setup pull request testing and linting checks. [Start here.](https://github.com/github/super-linter)
- API: Look into Python dependency managment patterns. [Start here.](https://kennethreitz.org/essays/2016/02/25/a-better-pip-workflow)
- API: Unit tests should be added in addition to the existing integration tests.
- API: More comprehensive DynamoDB error handling should be put in place.
- API: DynamoDB query pagination could be added to support things like infinite scrolling.
- UI: Looking into reducing bundle size with [babel-plugin-import](https://www.npmjs.com/package/babel-plugin-import)
- UI: More comprehensive API error handling should be put in place.
- UI: `react-query` uses some pretty aggresive refetching of stale data these settings could be tuned down.
- UI: The copy in the UI should really be templatized for localization support.
- UI: Accessibility was not really a consideration as I built out the UI. Screen reader landmarks and keyboard controls along with things like color contrast all should be considered.
- UI: The UI has no tests. I just ran out of time. My React skills were very rusty going into this.
