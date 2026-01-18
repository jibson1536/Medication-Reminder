from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["Medication Reminder_db"]   # change name if needed
