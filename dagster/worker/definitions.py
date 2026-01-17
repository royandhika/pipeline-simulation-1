from dagster import (
    Definitions, 
    asset, 
    EnvVar,
    MaterializeResult,
    DailyPartitionsDefinition,
    AssetExecutionContext,
)
from dagster_dbt import (
    DbtCliResource, 
    dbt_assets, 
    DbtProject, 
)
from resources import SFTPResource, PostgreResource

@asset(
    partitions_def=DailyPartitionsDefinition(
        start_date="2026-01-01",
        timezone="Asia/Jakarta"
    ),
    kinds={"postgres", "python"},
    key_prefix="raw"
)
def raw_data(context: AssetExecutionContext, sftp: SFTPResource, postgres: PostgreResource):
    """
    Reads a CSV from SFTP using the configured resource and writes to Postgres.
    """
    date = context.partition_key

    csv_path = f"upload/tweets-data/jakarta_hujan_since-{date}_until-2026-01-13_13-01-2026_20-31-55.csv"
    
    # Read from SFTP
    df = sftp.read_csv(csv_path)
    
    # Write to Postgres
    postgres.write_table(df, table_name="raw_data", if_exists="append")
    
    yield MaterializeResult(
        metadata={
            "row_count": len(df),
        }
    )

manifest = DbtProject(
        project_dir="dbt",
        profiles_dir="dbt",
        profile="postgre"
    ).manifest_path

@dbt_assets(
    manifest=manifest,
    select="processed_data",
    partitions_def=DailyPartitionsDefinition(
        start_date="2026-01-01",
        timezone="Asia/Jakarta"
    ),
)
def processed_data(context: AssetExecutionContext, dbt: DbtCliResource):
    run_arg = ["build"]

    yield from (
        dbt.cli(run_arg, context=context)
        .stream()
        .fetch_row_counts()
        .fetch_column_metadata()
    )

@dbt_assets(
    manifest=manifest,
    select="summary",
    partitions_def=DailyPartitionsDefinition(
        start_date="2026-01-01",
        timezone="Asia/Jakarta"
    ),
)
def summary(context: AssetExecutionContext, dbt: DbtCliResource):
    run_arg = ["build"]

    yield from (
        dbt.cli(run_arg, context=context)
        .stream()
        .fetch_row_counts()
        .fetch_column_metadata()
    )


defs = Definitions(
    assets=[raw_data, processed_data, summary],
    resources={
        "sftp": SFTPResource(
            host="sftp",
            username=EnvVar("SFTP_USER"),
            password=EnvVar("SFTP_PASS"),
        ),
        "postgres": PostgreResource(
            host="db",
            username=EnvVar("POSTGRES_USER"),
            password=EnvVar("POSTGRES_PASSWORD"),
            database=EnvVar("POSTGRES_DB"),
        ),
        "dbt": DbtCliResource(
            project_dir="dbt",
            profiles_dir="dbt",
            profile="postgre"
        )
    },
)