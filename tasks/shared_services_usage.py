from tasks.aws_redshift_connector import RedShift_Connector
from tasks.aws_secrets_manager_access import AWSSecretsManagerAccess
from tasks.utitlity_functions_redshift import getsharedServiceConfigDetails
import logging
import json
import sys
import requests
import time

def shared_services_usage(**kargs):
    res_dict,cursor = getsharedServiceConfigDetails()
    load_usage_data_if_source_is_API(res_dict,cursor)

def load_usage_data_if_source_is_API(res_dict,cursor):
        if (res_dict['usage_source']):
          usage_src_dict = res_dict['usage_source']
          service_names = res_dict['service_name']
          nth_index_to_load = 0
          DictIterations = 0
          for attribute in zip(service_names, usage_src_dict):
            nth_index_to_load += 1
            logging.info(nth_index_to_load)
            usage_dict = json.loads(attribute[1])
            service_name = attribute[0]
            logging.info(service_name)

            if usage_dict['type'] == 'API':
                logging.info("DictIterations")
                logging.info(DictIterations)

                DictIterations += 1
                api_endpoint_token = usage_dict['api-endpoint-token']
                api_search_command = usage_dict['api-search-command']
                api_endpoint_data = usage_dict['api-endpoint-data']
                api_path = usage_dict['vault-api-path']
                # API Data Load for
                load_usage_data_if_source_is_API(
                    api_endpoint_token, api_search_command, api_endpoint_data, api_path,cursor)

def load_usage_data_if_source_is_API(api_endpoint_token, api_search_command, api_endpoint_data, api_path,cursor):

    try:
        data = getsharedServiceConfigDetails.get_data(api_endpoint_token, api_search_command,
                    api_endpoint_data,api_path)

        insert_query_columns = """INSERT INTO dev.public.shared_services_usage(
                metric_date, cost_center_id, usage_metric_units, primary_metric_dimension, secondary_metric_dimension, service_name
                    ) VALUES"""
        for row in data:
            noOfRows += 1
            values += """('{}','{}','{}','{}','{}','{}','{}'),""".format(
                row['metric_date'],
                int(row["cost_center_id"]), 
                row['usage_metric_units'],
                row['primary_metric_dimension'],
                row["secondary_metric_dimension"], 
                row["service_name"])
        qry_str_insert = insert_query_columns+values+";"
        qry_str_insert = qry_str_insert[:-2] + \
        qry_str_insert[len(qry_str_insert)-1:]
        cursor.execute(qry_str_insert)
    except Exception as exc:
        logging.info("!!!!!!!!!!!!!!!!!Exception !!!!!!!!!!!!!!!!!!!!!!!")
        logging.info(exc)
        sys.exit()


