<p align="center"><a>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original-wordmark.svg" width="140"/>
</a></p>

## Description

The SAR Core Microservice is the incharge of provide some of the most important capabilities of the SAR system, as wastes collect request management, waste management and clients management.

## Context

The SAR system (by its initials in spanish Sistema de Gestión de Residuos) is a guvernamental scope fictitious enterprise system, SAR was proposed as one of the software focused projects of the AESOF specialization from the Pontificia Universidad Javeriana that i studied during 2023 and 2024, its main objective more than develop a full enterprise system was to improve technicals, design and methodological skills through the practice. The system main functional objective is to attend the need of having a unique centralized software that allows the governments that adopt them to easily manage radioactive wastes off all kinds from radiographies wastes to nuclear wastes and also cooperate with private enterprises that act as strategic partners between other needed capabilities, cause the project was develop as part of a architecture postgraduate project its main focus is in the architectural requirements not in the funcional ones.

## Dependencies

The project is mainly based on python but it include artifacts created with other technologies for different purposes such was some shortcuts and git hooks created with NodeJs and Shell scripts that automate some process like code formatting or commit linting when a commit is made the project also include load tests and smoke tests based on K6 and pure JavaScript and manifests written in yml for docker, docker compose and kubernetes, if you are going just to run the project you don't need all the dependencies, but if you are going to contribute to the project development all the dependencies next listed are needed.

- **NodeJs-v20.8.0**: Used for creating shortcuts and githooks
- **Python-3.12.0**: Used as the main project technologie
- **Poetry-1.8.2**: Used for env creation and python package management
- **Docker-26.0.0**: Used for cloud and local deployments
- **K6-v0.50.0**: Used for load and smoke testing

## Related Artifacts

- [**env_files**](https://drive.google.com/drive/folders/1PNMv2e0gqUWbSapvU-GirsTy_lvvbbIi?usp=sharing)

## Related Repositories

- [**sar_core_ms_ci**](https://github.com/joseesco24/sar_core_ms_ci)
- [**sar_core_ms_cd**](https://github.com/joseesco24/sar_core_ms_cd)
- [**sar_db_mysql**](https://github.com/joseesco24/sar_bd_mysql)
- [**sar_brms**](https://github.com/joseesco24/sar_brms)

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
