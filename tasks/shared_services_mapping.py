from tasks.aws_redshift_connector import RedShift_Connector
from tasks.aws_secrets_manager_access import AWSSecretsManagerAccess
from tasks.utitlity_functions_redshift import getsharedServiceConfigDetails
import logging
import json
import sys
import requests
import time

def shared_services_mapper(**kargs):
    res_dict,cursor = getsharedServiceConfigDetails()
    load_mapping_data_if_source_is_API(res_dict,cursor)

def load_mapping_data_if_source_is_API(res_dict,cursor):
        if (res_dict['mapping_source']):
        # mapping_sources = {res_dict['mapping_source']}
         mapper_src_dict = res_dict['mapping_source']
         service_names = res_dict['service_name']
         for attribute in zip(service_names, mapper_src_dict):
            mapper_dict = json.loads(attribute[1])

            if mapper_dict['type'] == 'API':
                api_endpoint_token = mapper_dict['api-endpoint-token']
                api_search_command = mapper_dict['api-search-command']
                api_endpoint_data = mapper_dict['api-endpoint-data']
                api_path = mapper_dict['api-path']
                # API Data Load for
                loadMapperDataOnRedShift(
                    api_endpoint_token, api_search_command, api_endpoint_data, api_path,cursor)

def loadMapperDataOnRedShift(api_endpoint_token, api_search_command, api_endpoint_data, api_path,cursor):

    try:
        data = getsharedServiceConfigDetails.get_data(api_endpoint_token, api_search_command,
                    api_endpoint_data,api_path)

        insert_query_columns = """INSERT INTO dev.public.shared_services_mapper(
                primary_metric_dimension, secondary_metric_dimension, cost_center_id, account_id
                    ) VALUES"""
        for row in data:
            noOfRows += 1
            values += """('{}','{}','{}','{}'),""".format(row["primary_metric_dimension"], row["secondary_metric_dimension"], int(
                row["cost_center_id"]) , int(row["account_id"]))
        qry_str_insert = insert_query_columns+values+";"
        qry_str_insert = qry_str_insert[:-2] + \
        qry_str_insert[len(qry_str_insert)-1:]
        cursor.execute(qry_str_insert)
    except Exception as exc:
        logging.info("!!!!!!!!!!!!!!!!!Exception !!!!!!!!!!!!!!!!!!!!!!!")
        logging.info(exc)
        sys.exit()


