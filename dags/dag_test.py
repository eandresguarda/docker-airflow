from airflow import DAG
from airflow.providers.postgres.operators.postgres import PythonOperator
from datetime import datetime, timedelta

from trading_bot.example import test

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

with DAG('TEST-Python', default_args=default_args, schedule_interval='0 */1 * * *', max_active_runs=1) as dag:
#dag = DAG("tutorial", default_args=default_args, schedule_interval='*/5 * * * *')

    t1 = PythonOperator(task_id='ejemplo', python_callable = test)