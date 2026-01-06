# Data Engineering Simulation

This project simulates a data ingestion and storage environment using Docker. It currently establishes a source system (SFTP) and a data warehouse (PostgreSQL).

## Services

### 1. Source System: SFTP Server (`atmoz/sftp`)
*   **Function:** Simulates an external system providing raw data files.
*   **Local Storage:** Files are persisted in the `./upload` directory.
*   **Internal Path:** Mapped to `/home/admin/upload` inside the container.
*   **Access:** Port `2222`.

### 2. Storage System: PostgreSQL (`postgres:alpine`)
*   **Function:** Serves as the central Data Warehouse.
*   **Persistence:** Data is stored in `./postgres_data/warehouse`.
*   **Initialization:** Automatically creates schemas defined in `./postgres_data/init.sql`.
*   **Access:** Port `5433`.

## Database Schemas
The database `warehouse` is initialized with the following schemas:
1.  `raw`: For landing raw data as-is from the source.
2.  `staging`: For intermediate data processing.
3.  `mart`: For business-ready analytic tables.

## Quick Start

### 1. Environment Configuration
The project is configured via `.env`. Default credentials:

| Service | Variable | Value |
| :--- | :--- | :--- |
| **SFTP** | User | `sftpuser` |
| | Password | `sftppass` |
| | Port | `2222` |
| **Postgres** | User | `postgresuser` |
| | Password | `postgrespass` |
| | DB Name | `warehouse` |
| | Port | `5433` |

### 2. Run the Project
Start the services in detached mode:
```bash
docker-compose up -d
```

### 3. Verify Connections

**Connect to SFTP:**
```bash
sftp -P 2222 sftpuser@localhost
```

**Connect to Database:**
Use any client with port **5433**.
```bash
psql -h localhost -p 5433 -U postgresuser -d warehouse
```

## Resetting the Environment
To completely reset the database (wiping all data and recreating schemas):

```bash
docker-compose down
sudo rm -rf postgres_data/warehouse
docker-compose up -d
```

## Future Roadmap
*   **Dagster Integration:** To be added as a worker/orchestrator to automate the ETL process from SFTP to PostgreSQL.