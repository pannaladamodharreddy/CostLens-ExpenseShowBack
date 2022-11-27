# This is the test File Using this to test testing the connector 
# plugins and few examples on calculating business logic

def A():
    test1 = 1
    test2 = 2
    return test1, test2

a, b = A()
print(b)

import json

import json
d =['{"type": "API", "filename": "", "api-endpoint-token": "https://aaa.net:8089/services/search/jobs/search/jobs", "api-search-command": "| inputlookup/costcenters.csv/", "api-endpoint-data": "https://aaaa.net:8089/services/search/jobs/services/search/jobs/{sid}/results/?count=0&output_mode=json"}', '{"type": "FILE", "filename": "mapping.csv", "api-endpoint-token": "", "api-endpoint-data": ""}']

for i in d:
        dict = json.loads(i)
        if dict['type'] == "API":
                print(dict)
sid = 1   
api_endpoint_data = "{sid}Hi"
api_endpoint_data.replace("{sid}",str(sid))
print(api_endpoint_data.replace("{sid}",str(sid)))

l = [{'date': '2022-07-19', 'index': 'aam', 'ingestSizeGB': '3060.600754870', 'ccenter': '1000011', 'report': 'Ingest'}, {'date': '2022-07-19', 'index': 'aam_hubble', 'ingestSizeGB': '527.084795499', 'ccenter': '100089890', 'report': 'Ingest'}]
print(l[0]['date'])
print(l[0]['report'])

print(type(1).__name__)


finalList = []
keys = ['service_name', 'contact_email', 'allocation_model',
        'metric_measure', 'metric_units', 'spend_cadence']
shared_service_values = ['service_1', 'dpannala@gmail.com', 'USAGE', 'MEMORY', 'GB, MB',
                         'DAILY', 'service_2', 'dpannala@gmail.com', 'USAGE', 'MEMORY', 'GB, MB', 'DAILY']
count = int(len(shared_service_values)/len(keys))
counter = 0
for i in range(0, int(len(keys))):  # Iterate All Columns 9 times iteration
    #Combine Lists of Lists 3 times iteration
    for j in range(0, int(len(shared_service_values)/len(keys))):
        testlist.append(shared_service_values[counter])
        counter += (len(keys))
    counter = i+1
    print(testlist)
    finalList.append(testlist)
    count += 1
    testlist = []
res_dict = dict(zip(keys, finalList))
print(res_dict)