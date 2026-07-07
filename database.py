from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://prepwise:Nishant%40123@cluster0.cgvptbb.mongodb.net/ai_pdf?retryWrites=true&w=majority"
)

db = client["ai_pdf"]

users = db["users"]
summaries = db["summaries"]

users.create_index("username", unique=True)