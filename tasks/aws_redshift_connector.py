import redshift_connector
import tasks.aws_secrets_manager_access as AWSSecretsManagerAccess

# Connects to Redshift cluster using AWS credentials
class RedShift_Connector:

    def __init__(self):
        print("2. Initialize the new instance of Point.")
        secretsManagerInstance = AWSSecretsManagerAccess()
        secretsManagerInstanceCred = secretsManagerInstance.get_secret_creds(
        "resdhift-dev")
        self.host = secretsManagerInstanceCred['host']
        self.database = 'dev'
        self.user = secretsManagerInstanceCred['username']
        self.password = secretsManagerInstanceCred['password']
        self.autoCommit = True

    def  connectToRedShift(self):
        conn = redshift_connector.connect(
        host=self.host,
        database=self.database,
        user=self.user,
        password=self.password
        )
        conn.autocommit = self.autoCommit
        cursor: redshift_connector.Cursor = conn.cursor()
        return cursor
    def loadSharedServiceConfigRows(self):
        redshift_connector_instance =  RedShift_Connector()
        cursor = redshift_connector_instance.connectToRedShift()
        selectConfigDetails = """
        select * from dev.public.shared_services_configurator
          """
        cursor.execute(selectConfigDetails)
        shared_service_config_data: tuple = cursor.fetchall()
        return shared_service_config_data


    

        


