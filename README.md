# Turbocharging-Retail-Insights: E-Commerce data pipeline

## Project Overview

This project showcases a robust data pipeline tailored for online retail, built on Apache Airflow and leveraging Google Cloud Platform (GCP) for data storage, processing, and visualization.

## Key Features

- **Automated Data Flow**: Effortlessly move data from GCP buckets to BigQuery.
- **Data Quality Assurance**: Ensure data accuracy with Soda's data integrity checks.
- **Flexible Data Transformations**: Leverage dbt's SQL capabilities for data manipulation.
- **Actionable Insights**: Gain insights from clear visualizations through Metabase dashboards.

## Getting Started

### Prerequisites

- **Astro CLI**: Utilize Astro CLI for a user-friendly Apache Airflow interface.
- **GCP Ecosystem**: Leverage GCP's Bucket and BigQuery for data management.

### Essential Tools

- Astro Runtime: `quay.io/astronomer/astro-runtime:8.8.0`
- Soda Core BigQuery: `soda-core-bigquery==3.0.45`
- Soda Core Scientific: `soda-core-scientific==3.0.45`
- dbt BigQuery: `dbt-bigquery==1.5.3`

## Resources

- [Astro CLI Documentation](https://www.astronomer.io/docs/)
- [Soda.io Documentation](https://docs.soda.io/)
- [Cosmos by Astronomer](https://www.astronomer.io/)

This project was inspired by the tutorial: [Data Engineer Project: An end-to-end Airflow data pipeline with BigQuery, dbt Soda, and more!](https://www.youtube.com/watch?v=DzxtCxi4YaA) by Marc Lamberti.
