import json
import urllib.parse
import boto3
import json
import yaml
import csv

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        result = response['Body'].read().decode('utf-8')
        parsed_yaml = yaml.safe_load(result)
        service_name = ''
        mapping_source = ''
        usage_source = ''
        spend_source = ''
        
        if parsed_yaml:
            service_name =  parsed_yaml['service-name']
            mapping_source = json.dumps(parsed_yaml['mapping-source'])
            usage_source = json.dumps(parsed_yaml['usage-source'])
            spend_source = json.dumps(parsed_yaml['spend-source'])
            metric_units = [i if len(parsed_yaml['metric-units'])<2 else i.replace("'","") for i in parsed_yaml['metric-units']]
        session = boto3.session.Session()
        region = session.region_name
        
        secret_name = ""
        print(parsed_yaml)
        
        secret_name = 'resdhift-dev'
        client = session.client(
            service_name = 'secretsmanager',
            region_name = region
            )
        secret_name = "resdhift-dev"
        region_name = "us-east-1"

        session = boto3.session.Session()
        client = session.client(
        service_name='secretsmanager',
        region_name=region_name
        )
            
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
        secret_arn = get_secret_value_response['ARN']
        secret = get_secret_value_response['SecretString']
        secret_json = json.loads(secret)
        cluster_id =  secret_json['dbClusterIdentifier']
        
        client_redshift = boto3.client('redshift-data')
        
        qry_str_delete =  f"""delete FROM dev.public.shared_services_configurator 
        where service_name =  '{service_name}';"""
        
        print(qry_str_delete)
        
        
        client_redshift.execute_statement(ClusterIdentifier = cluster_id,
                                          Database = 'dev',
                                          SecretArn = secret_arn, Sql = qry_str_delete)
        qry_str_insert = """insert into dev.public.shared_services_configurator values
        ('{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(
            parsed_yaml['service-name'],
            parsed_yaml['contact-email'],
            parsed_yaml['allocation-model'],
            parsed_yaml['metric-measure'],
            ', '.join(metric_units),
            parsed_yaml['spend-cadence'],
            mapping_source,
            spend_source,
            usage_source
            )
        print(qry_str_insert)
        result = client_redshift.execute_statement(ClusterIdentifier = cluster_id,
                                      Database = 'dev',
                                          SecretArn = secret_arn, Sql = qry_str_insert)
        result1 = client_redshift.execute_statement(ClusterIdentifier = cluster_id,
                                          Database = 'dev',
                                         SecretArn = secret_arn, Sql = 'select * from dev.public.shared_services_configurator')                               
                                          
        print("++++++++++++++",result)
        print('=================>>>>>>>>',result1,'++++++++')
        commit = 'commit transaction;'
        client_redshift.execute_statement(ClusterIdentifier = cluster_id,
                                          Database = 'dev',
                                        SecretArn = secret_arn, Sql = commit)
        
       
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
