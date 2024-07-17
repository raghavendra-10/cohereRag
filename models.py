from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize MongoDB client and define the database and collection
client = MongoClient("mongodb+srv://raghavendra:PLSjBgrRYmEdGlbz@cluster0.iktswhw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['your_database_name']
collection = db['health_data']

# Define a function to save data to MongoDB
def save_data(patientId, data):
    new_data = {"patientId": patientId, "data": data}
    collection.insert_one(new_data)

# Define a function to retrieve documents from MongoDB
def retrieve_documents(patientId):
    results = collection.find({"patientId": patientId})
    documents = []
    for result in results:
        res = result['data']
        for key, value in res.items():
            if isinstance(value, list):
                for item in value:
                    documents.append({"title": key, "text": item['answer']})
            else:
                documents.append({"title": key, "text": str(value)})
    return documents
