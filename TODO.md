# Project Roadmap & TODO

## 🎯 Milestone 1: Core Infrastructure (Completed)
- [x] Set up SFTP container as data source.
- [x] Set up PostgreSQL container as data warehouse.
- [x] Initialize database schemas (`raw`, `staging`, `mart`).
- [x] Document project in README.md.

## 🚀 Milestone 2: Orchestration with Dagster
Goal: Set up Dagster to manage data pipelines between SFTP and Postgres.

- [x] **Dockerization**
    - [x] Create a robust `Dockerfile` for Dagster components.
    - [x] Include necessary Python libraries (`dagster-postgres`, `dagster-webserver`, `pandas`, `paramiko` for SFTP).
- [x] **Configuration**
    - [x] Set up `dagster.yaml` for persistent storage in PostgreSQL.
    - [x] Set up `workspace.yaml` to manage code locations.
- [x] **Service Deployment (Docker Compose)**
    - [x] Add `dagster-webserver` service.
    - [x] Add `dagster-daemon` service for scheduling and sensors.
    - [x] Add code-location service (User Code).
- [ ] **Pipeline Development**
    - [ ] Create a sensor to detect new files in SFTP `upload/` folder.
    - [ ] Build an Asset/Job to move data from SFTP to Postgres `raw` schema.

## 🛠 Maintenance & Improvements
- [/] Add health checks to Docker services (DB added).
- [ ] Implement automated backups for `postgres_data`.
- [ ] Set up network isolation between containers.
