from pymongo import MongoClient, ReadPreference
from pymongo.errors import OperationFailure

# Replace with your MongoDB connection string, including username and password
uri = "mongodb://mongoadmin:password@localhost:27017/?directConnection=true"

try:
    # Step 1: Establish a connection to the MongoDB server with authentication
    client = MongoClient(uri)
    client.admin.command('ping')  # Verify the connection

    # Step 2: Select the database and collection
    db = client['test_db']
    collection = db['test_collection']

    # Step 3: Prepare the data to be inserted
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
    }

    # Step 4: Insert the data into the collection
    result = collection.insert_one(data)

    # Print the ID of the inserted document
    print(f"Data inserted with id {result.inserted_id}")

    # Fetch all documents
    documents = collection.find()

    for doc in documents:
        print(doc)

except OperationFailure as e:
    print(f"Operation failed: {e}")
finally:
    # Step 5: Close the connection
    client.close()