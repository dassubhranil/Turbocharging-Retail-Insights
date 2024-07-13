from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType

@dag(
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=['retail'],
)
def retail():
    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',
        src='include/dataset/online_retail.csv',
        dst='raw/online_retail.csv',
        bucket='dassubhranil_online_retail',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )

    create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        dataset_id='retail',
        gcp_conn_id='gcp',
    )

    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://dassubhranil_online_retail/raw/online_retail.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='raw_invoices',
            conn_id='gcp',
            metadata=Metadata(schema='retail')
        ),
        use_native_support=False,
    )

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    # check_load()

    # # Read SQL query from an external file
    with open('/usr/local/airflow/include/dbt/models/sources/retail_country_table_creation.sql', 'r') as file:
        sql_creation_query = file.read()

    # Task for creating the table
    create_country_table = BigQueryExecuteQueryOperator(
        task_id='create_country_table',
        sql=sql_creation_query,  # Adjust path as needed
        gcp_conn_id='gcp',  # Use your correct GCP connection ID
        use_legacy_sql=False,
    )

    with open('/usr/local/airflow/include/dbt/models/sources/retail_country_table_insertion.sql', 'r') as file:
        sql_insertion_query = file.read()

    # Task for inserting data into the table
    insert_into_country_table = BigQueryExecuteQueryOperator(
        task_id='insert_into_country_table',
        sql=sql_insertion_query,  # Adjust path as needed
        gcp_conn_id='gcp',  # Use your correct GCP connection ID
        use_legacy_sql=False,
    )
    transform = DbtTaskGroup(
        group_id='transform',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/transform']
        ),
    )

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform ', checks_subpath='transform'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    # check_transform()

    report = DbtTaskGroup(
        group_id='report',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/report']
        ),
    )

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_report(scan_name='check_report', checks_subpath='report'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    # check_report()

    chain(
        upload_csv_to_gcs,
        create_retail_dataset,
        gcs_to_raw,
        check_load(),
        create_country_table,
        insert_into_country_table,
        transform,
        check_transform(),
        report,
        check_report(),
    )

retail()