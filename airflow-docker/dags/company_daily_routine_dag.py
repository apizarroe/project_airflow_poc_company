from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.smtp.operators.smtp import EmailOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

# Argumentos específicos para Company Daily Routine
company_daily_routine_args = {
    'owner': 'company',
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 0,  # Sin reintentos automáticos
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
with DAG(
    'company_daily_routine',
    default_args=company_daily_routine_args,
    description='DAG para rutina diaria de Company',
    schedule=None,  # Se ejecuta manualmente
    start_date=datetime(2025, 1, 1),
    catchup=False,
    is_paused_upon_creation=False,  # DAG activo (ON) al crearse
    tags=['company', 'routine'],
) as dag:

    # ===== Tarea 1: Inicio de rutina =====
    inicio_rutina = BashOperator(
        task_id='inicio_rutina',
        bash_command='echo "Inicio de Rutina"',
    )

    inicio_rutina_email_success = EmailOperator(
        task_id='inicio_rutina_email_success',
        to='apizarro_13@hotmail.com',
        subject='[Company] Inicio de Rutina - Éxito',
        html_content='<p>La tarea <strong>inicio_rutina</strong> se completó exitosamente.</p>',
        trigger_rule='all_success',
    )

    inicio_rutina_email_failure = EmailOperator(
        task_id='inicio_rutina_email_failure',
        to='apizarro_13@hotmail.com',
        subject='[Company] Inicio de Rutina - Fallo',
        html_content='<p>La tarea <strong>inicio_rutina</strong> falló.</p>',
        trigger_rule='one_failed',
    )

    # ===== Tarea 2: Disparar DAG de procesamiento de datos =====
    trigger_process_data_dag = TriggerDagRunOperator(
        task_id='trigger_process_data_dag',
        trigger_dag_id='company_process_data',
        wait_for_completion=True,  # Espera a que el DAG triggereado termine
        poke_interval=30,  # Revisa cada 30 segundos
    )

    # ===== Dependencias =====
    inicio_rutina >> [inicio_rutina_email_success, inicio_rutina_email_failure]
    inicio_rutina >> trigger_process_data_dag
