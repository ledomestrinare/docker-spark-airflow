import airflow
from datetime import timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',    
    'retry_delay': timedelta(minutes=5),
}

spark_dag = DAG(
        dag_id = "RM_PFUNC",
        default_args=default_args,
        schedule_interval=None,	
        dagrun_timeout=timedelta(minutes=60),
        description='Carregamento de tabelas do RM',
        start_date = airflow.utils.dates.days_ago(1)
)

Extract = SparkSubmitOperator(
        task_id="RM_PFUNC",
        application="/opt/airflow/dags/RM/RM_PFUNC.py",
        conn_id="spark_local",
    #     conf={
    #     "spark.master": "spark://spark-master:7077",
    #     "spark.submit.deployMode": "client"
    # },
        dag=spark_dag
)

Extract