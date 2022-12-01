from tasks.aws_redshift_connector import RedShift_Connector
from tasks.aws_secrets_manager_access import AWSSecretsManagerAccess
from tasks.utitlity_functions_redshift import getsharedServiceConfigDetails
import logging
import json

def shared_services_showback_costs(**kargs):
    res_dict,cursor = getsharedServiceConfigDetails()
    calculateShowBackCosts(res_dict,cursor)

def loadMapperData(cursor):
    pass

def loadSpendData(cursor):
    pass

def loadUsageData(cursor):
    pass

def calculateShowBackCosts(res_dict,cursor):
    pass



