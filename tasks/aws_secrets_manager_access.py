""" AWS Secrets Manager Connector"""
import logging
import json
from os import environ as env
import boto3
from botocore.exceptions import ClientError


class AWSSecretsManagerAccess():
    """ AWS Secrets Manager Connector"""

    def __init__(self):
        """ Constructor to Load required parameters to create the instance"""
        self._session = boto3.session.Session()
        self.client = self._session.client(
            service_name='secretsmanager',
            aws_access_key_id='AKIAXRU37AQXMAXCLTO3',
            aws_secret_access_key='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',
            region_name='us-east-1'
        )

    def get_secret_creds(self, secret_name=None):
        """Fetch Splunk Creds from AWS Secrets Manager"""

        secret_name = "resdhift-dev"
        logging.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logging.info(self.client)
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
            splunk_secret_creds = json.loads(
                get_secret_value_response['SecretString'])
            return splunk_secret_creds
        except ClientError as exc:
            raise exc

secrets_manager_instance = AWSSecretsManagerAccess()
splunk_secret_creds = secrets_manager_instance.get_splunk_secret_creds(
        "resdhift-dev")
print(splunk_secret_creds)
