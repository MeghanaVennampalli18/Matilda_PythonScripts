from pymongo import MongoClient
client = MongoClient("mongodb://admin:Matilda7%23@172.24.6.190:30020")
db = client['matildacost']
collection = db['mcost_aws_rc']

# query = {'service':'observability'}
# query = {'serviceName':'ObservabilityMonitoring'}
# query = {
#     "$or": [
#         {"name": "Oracle Cloud Infrastructure - Logging - Storage"},
#         {"name": "Monitoring - Ingestion"},
#         {"name": "Monitoring - Retrieval"},
#     ]
# }

arr=set()
documents = collection.find()
for document in documents:
    arr.add(document.get('serviceType'))
    # print(document.get('name'))
print(arr)    


# documents = collection.find()
# for document in documents:
#     service_name = document.get('serviceName', 'N/A') 
#     name = document.get('name', 'N/A')  
#     combined = f"serviceName: {service_name}, name: {name}"
#     print(combined)


# documents = collection.find()
# unique_services = set()
# for document in documents:
#     print(document.get('name'))
#     unique_services.add(document.get('serviceName'))
# print(unique_services)



client.close() 