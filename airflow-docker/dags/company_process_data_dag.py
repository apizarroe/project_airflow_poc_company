from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.smtp.operators.smtp import EmailOperator

# Importar función de procesamiento de datos desde archivo externo
from scripts.process_data import process_company_data

# Argumentos específicos para Company Process Data
company_process_data_args = {
    'owner': 'company',
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 0,  # Sin reintentos automáticos
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
with DAG(
    'company_process_data',
    default_args=company_process_data_args,
    description='DAG de procesamiento de datos - Se ejecuta después de company_daily_routine',
    schedule=None,  # Se ejecuta manualmente o triggereado por otro DAG
    start_date=datetime(2025, 1, 1),
    catchup=False,
    is_paused_upon_creation=False,  # DAG activo (ON) al crearse
    tags=['company', 'process'],
) as dag:

    # Tarea: Procesamiento de datos
    process_data_task = PythonOperator(
        task_id='process_data_task',
        python_callable=process_company_data,
    )

    process_data_email_success = EmailOperator(
        task_id='process_data_email_success',
        to='apizarro_13@hotmail.com',
        subject='[Company] Procesamiento de Datos - Éxito',
        html_content='<p>La tarea <strong>process_data_task</strong> se completó exitosamente.</p>',
        trigger_rule='all_success',
    )

    process_data_email_failure = EmailOperator(
        task_id='process_data_email_failure',
        to='apizarro_13@hotmail.com',
        subject='[Company] Procesamiento de Datos - Fallo',
        html_content='<p>La tarea <strong>process_data_task</strong> falló.</p>',
        trigger_rule='one_failed',
    )

    # Dependencias
    process_data_task >> [process_data_email_success, process_data_email_failure]
