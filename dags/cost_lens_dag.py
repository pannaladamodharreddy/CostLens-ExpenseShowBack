# We'll start by importing the DAG object
from airflow import DAG
# We need to import the operators used in our tasks
from airflow.operators.python_operator import PythonOperator
# We then import the days_ago function
from airflow.utils.dates import days_ago

from airflow.models import Variable
import datetime

import logging

from tasks.aws_redshift_connector import RedShift_Connector
from tasks.shared_services_mapping import shared_services_mapper
from tasks.shared_services_usage import shared_service_usage
from tasks.shared_services_spend import shared_service_spend


# initializing the default arguments that we'll pass to our DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime.utcnow(),
    'email': ['pannaladamoderreddy@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
}
# CMSU - Config Mapper Spend Usage
load_costlens_cmsu_data = DAG(
    'load_config_data',
    default_args=default_args,
    description='config_data',
    schedule_interval= '@daily',
)

def push_function(**context):
    shared_service_config_details=load_config_data()
    task_instance = context['task_instance']
    task_instance.xcom_push(key="ServiceConfigDetails", value=shared_service_config_details)

def pull_config_details_via_xcom(**kwargs):
    ti = kwargs['ti']
    resultRows = ti.xcom_pull(task_ids='push_task',key='ServiceConfigDetails')

def load_config_data():
    redshift_connector_instance =  RedShift_Connector
    shared_service_config_details = redshift_connector_instance.loadSharedServiceConfigRows()
    logging.info(shared_service_config_details)
    return shared_service_config_details

def validate_load_mapper_data(shared_service_config_details):
    shared_services_mapper(shared_service_config_details)
    
def validate_load_usage_data(shared_service_config_details):
    shared_service_usage(shared_service_config_details)

def validate_load_spend_data(shared_service_config_details):
    shared_service_spend(shared_service_config_details)

def calculate_showback_costs():
    pass


load_config = PythonOperator(
    task_id='load_config',
    python_callable = push_function,
    dag=load_costlens_cmsu_data
)
load_mapper = PythonOperator(
    task_id='load_mapper',
    python_callable = validate_load_usage_data(pull_config_details_via_xcom),
    dag=load_costlens_cmsu_data
)
load_usage = PythonOperator(
    task_id='load_usage',
    python_callable = validate_load_usage_data(pull_config_details_via_xcom),
    dag=load_costlens_cmsu_data
)
load_spend = PythonOperator(
    task_id='load_spend',
    python_callable = validate_load_spend_data(pull_config_details_via_xcom),
    dag=load_costlens_cmsu_data
)

calculate_showback_costs = PythonOperator(
    task_id='calculate_showback_costs',
    python_callable = validate_load_spend_data(pull_config_details_via_xcom),
    dag=load_costlens_cmsu_data
)


load_config >> load_mapper >> load_usage >> load_spend >> calculate_showback_costs