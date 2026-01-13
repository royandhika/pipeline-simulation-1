from dagster import ConfigurableResource
from dagster_dbt import DbtCliResource
import paramiko
import pandas as pd
from contextlib import contextmanager
from sqlalchemy import create_engine

class SFTPResource(ConfigurableResource):
    host: str
    port: int = 22
    username: str
    password: str

    @contextmanager
    def get_client(self):
        transport = paramiko.Transport((self.host, self.port))
        try:
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            yield sftp
        finally:
            if transport:
                transport.close()

    def read_csv(self, remote_path: str, **kwargs) -> pd.DataFrame:
        """
        Reads a CSV file from SFTP directly into a Pandas DataFrame.
        kwargs are passed to pd.read_csv
        """
        with self.get_client() as sftp:
            with sftp.open(remote_path) as f:
                return pd.read_csv(f, **kwargs)

class PostgreResource(ConfigurableResource):
    host: str
    port: int = 5432
    username: str
    password: str
    database: str

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    def get_engine(self):
        """Returns a SQLAlchemy Engine. Useful for pandas.to_sql."""
        return create_engine(self.connection_string)

    @contextmanager
    def get_connection(self):
        """Yields a raw SQLAlchemy connection for executing SQL queries."""
        engine = self.get_engine()
        with engine.connect() as conn:
            yield conn

    def write_table(self, df: pd.DataFrame, table_name: str, if_exists: str = "replace", index: bool = False, **kwargs):
        """
        Writes a Pandas DataFrame to a PostgreSQL table.
        kwargs are passed to df.to_sql
        """
        engine = self.get_engine()

        # Add timestamp
        df["_timestamp"] = pd.Timestamp.now()
        
        # Write to SQL (default schema 'raw' for datalanding)
        df.to_sql(table_name, engine, schema="raw", if_exists=if_exists, index=index, **kwargs)

    