from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate_random_number():
    """Generate a random number and return it as JSON."""
    random_num = random.randint(1, 100)
    return jsonify({"random_number": random_num})