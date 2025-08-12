from flask import Flask, jsonify
import random
import os
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate_random_number():
    """Generate a random number and return it as JSON."""
    random_num = random.randint(1, 100)
    return jsonify({"random_number": random_num})

@app.route('/get_random_question', methods=['GET'])
def get_random_question():
    """Connect to MongoDB and return a random question as JSON."""
    uri = os.environ.get('MONGO_URI')
    if not uri:
        return jsonify({"error": "MongoDB URI not configured"}), 500
    
    try:
        client = MongoClient(uri)
        db = client['mcq']  # Database name from your notebook
        collection = db['test']  # Collection name from your notebook
        
        # Use aggregation to sample one random document
        pipeline = [{'$sample': {'size': 1}}]
        result = list(collection.aggregate(pipeline))
        
        if result:
            question = result[0]
            question.pop('_id', None)  # Remove MongoDB's internal _id field
            return jsonify(question)
        else:
            return jsonify({"error": "No questions found in the database"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        client.close()  # Close connection after use
