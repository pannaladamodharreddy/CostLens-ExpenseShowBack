from tasks.aws_redshift_connector import RedShift_Connector
from tasks.aws_secrets_manager_access import AWSSecretsManagerAccess
import logging
import json
import sys
import requests
import time

def shared_services_mapper(shared_service_values):

    redshift_cluster_instance =  RedShift_Connector()
    cursor  = redshift_cluster_instance.connectToRedShift()
    query = """
        select col_name from pg_get_cols('dev.public.shared_services_configurator')
        cols(view_schema name, view_name name, col_name name, col_type varchar, col_num int);
        """
    cursor.execute(query)
    tupled_keys = cursor.fetchall()
    keys = sum(tupled_keys, [])  # converting them to a list
    logging.info(keys)
    query = """
        SELECT service_name, contact_email, allocation_model, metric_measure, metric_units, spend_cadence, mapping_source, usage_source, spend_source,timestamp
FROM dev.public.shared_services_configurator;
        """
    cursor.execute(query)

    shared_service_values = sum(cursor.fetchall(), [])
    logging.info(shared_service_values)  # converting them to a list
    list_of_values = []
    list_of_values_list = []
    nth_index_to_load = int(len(shared_service_values)/len(keys))
    incrementer = 0
    # Storing Configurations to Dict from the Configurator Table for Validating & Data Load purpose
    # Assuming Cofig Table will be relatively small else The logic should be modified in a efficient way to reduce time complexity
    for i in range(0, int(len(keys))):  # Iterate All Columns in the Table
        # Iterate Through Row Values and store them as List of List
        for j in range(0, int(len(shared_service_values)/len(keys))):
            list_of_values.append(shared_service_values[incrementer])
            incrementer += (len(keys))
        incrementer = i+1
        list_of_values_list.append(list_of_values)
        nth_index_to_load += 1
        list_of_values = []
    res_dict = dict(zip(keys, list_of_values_list))
    # Configurator Table converted into a Dict for convenience
    logging.info(res_dict)

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
        data = get_data(api_endpoint_token, api_search_command,
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

def get_data(api_endpoint_token, api_search_command, api_endpoint_data, api_path, offset=None, report=None):
    secrets_manager_instance = AWSSecretsManagerAccess()
    secret_creds = secrets_manager_instance.get_secret_creds(
        api_path)
    attempt = 0
    attempt_limit = 10
    wait_time = 3
    try: 
         while attempt < attempt_limit:

          res = requests.post(api_endpoint_token,
                            data={
                                "search": api_search_command,
                                "output_mode": "json"},
                            auth=(secret_creds['username'], secret_creds['password']))
          if (
                    int(res.headers["Content-Length"]) != 0
                    and "results" in res.json()
                    and res.json()["results"]):
                data = res.json()["results"]
                break
            # no data was retrieved so let's wait and then try again
          if attempt < attempt_limit:
                time.sleep(wait_time)
                logging.info(data)
         return data
    except Exception as exc:
        logging.info(exc)
        sys.exit()

           






        