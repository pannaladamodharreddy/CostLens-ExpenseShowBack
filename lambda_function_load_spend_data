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
        csv_file = s3.get_object(Bucket=bucket, Key=key)
        s3_resource = boto3.resource('s3')
        s3_object = s3_resource.Object(bucket,key)
        data = s3_object.get()['Body'].read().decode('utf-8').splitlines()
        values = csv.reader(data)
        # Skip the headers from the values of CSV
        headers = next(values)
        
        #region
        session = boto3.sessionSession()
        region = session.region_name
        
        #secrets 
        secret_name = 'resdhift-dev'
        client = session.client(
            service_name = 'secretsmanager',
            region_name = region
            )
            
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
        secret_arn = get_secret_value_response['ARN']
        secret = get_secret_value_response['SecretString']
        secret_json = json.loads(secret)
        cluster_id =  secret_json['dbClusterIdentifier']
        
        client_redshift = boto3.client('redshift-data')
        
        qry_str_insert = ''
        for value in values:
            qry_str_insert+= """INSERT INTO dev.public.shared_Service_spend_data(metric_date,spend,primary_metric_dimension,account_id,service_name)
            values ('{}','{}','{}','{}','{}');
            """.format(*value)
        print(qry_str_insert)
        
        client_redshift.execute_statement(ClusterIdentifier = cluster_id,
                                          Database = 'dev',
                                          SecretArn = secret_arn, Sql = qry_str_insert)
       
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
