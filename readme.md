<p align="center"><a>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original-wordmark.svg" width="140"/>
</a></p>

## Description

This repository corresponds to the a small python microservice that is going to be used used in the sar system.

## Dependencies

The project is mainly based on python but it include artifacts created with other technologies for different purposes such was some shortcuts and git hooks created with NodeJs and Shell scripts that automate some process like code formatting or commit linting when a commit is made the project also include load tests and smoke tests based on K6 and pure JavaScript and manifests written in yml for docker, docker compose and kubernetes, if you are going just to run the project you don't need all the dependencies, but if you are going to contribute to the project development all the dependencies next listed are needed.

- **NodeJs-v20.8.0**: Used for creating shortcuts and githooks
- **Python-3.12.0**: Used as the main project technologie
- **Poetry-1.8.2**: Used for env creation and python package management
- **Docker-26.0.0**: Used for cloud and local deployments
- **K6-v0.50.0**: Used for load and smoke testing

## Related Repositories

- **sar_db_mysql:** https://github.com/joseesco24/sar_bd_mysql
- **sar_brms:** https://github.com/joseesco24/sar_brms

## Local Deployment

The project could be deployed locally using a docker command or a npm shortcut.

Using just docker.

```shell
docker compose -f ./docker-compose.yaml up
```

Using docker and npm.

```shell
npm run docker-start
```

## Project Installation

Assuming that you already counted with the required programming languages and software previously listed execute the next commands in order.

Project core dependencies installation.

```shell
poetry install
```

Project development dependencies installation.

```shell
npm install
```

<br/>
