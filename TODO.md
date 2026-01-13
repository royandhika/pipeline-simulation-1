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
    - [x] Include necessary Python libraries (`dagster-postgres`, `dagster-webserver`, `pandas`, `paramiko`, `sqlalchemy`).
- [x] **Configuration**
    - [x] Set up `dagster.yaml` for persistent storage in PostgreSQL.
    - [x] Set up `workspace.yaml` to manage code locations.
    - [x] Configure timezone (`TZ=Asia/Jakarta`) for consistent timestamps.
- [x] **Service Deployment (Docker Compose)**
    - [x] Add `dagster-webserver` service.
    - [x] Add `dagster-daemon` service for scheduling and sensors.
    - [x] Add code-location service (`worker`).
- [x] **Pipeline Development**
    - [x] Implement `SFTPResource` for secure file access.
    - [x] Implement `PostgreResource` for database operations with `sqlalchemy`.
    - [x] Create `raw_data` asset to move specific CSV from SFTP to Postgres `raw` schema.
    - [x] Add metadata logging (row count, preview) to assets.

## 🏃 Milestone 3: Advanced Pipeline Features (Next Steps)
- [ ] **Dynamic Sensors:** Create a sensor to detect *new* files in SFTP `upload/` folder automatically instead of hardcoding filenames.
- [ ] **Data Quality:** Add Dagster Asset Checks to verify data integrity (e.g., null checks).
- [ ] **dbt Integration:** Implement dbt project to transform data in `staging` and `mart`.

## 🛠 Maintenance & Improvements
- [x] Add health checks to Docker services (DB added).
- [/] Implement automated backups for `postgres_data`.
- [ ] Set up network isolation between containers.