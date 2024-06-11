from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from trading_bot.btc_bybit_demo import run_bollinger_strategy

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020,8,7),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on:retry":False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016,1,1),
}

with DAG('Bybit-BBands', default_args=default_args, schedule_interval='0 */4 * * *', max_active_runs=1) as dag:

    t1 = PythonOperator(task_id='Ejecutar_BBands', python_callable = run_bollinger_strategy)