import csv
import cohere
from flask import Flask, request, jsonify

# Initialize the Cohere client
client = cohere.Client(api_key='YOUR_API_KEY')
dataset = []
# Load dataset from CSV file
def load_dataset_from_csv(file_path):
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dataset.append(row)
    return dataset

# Define a function to generate API responses based on user query
def generate_api_response(query, dataset):
    print(dataset)
    try:
        # Use Cohere AI to generate API responses
        response = client.generate(
            prompt=query,
            max_tokens=500,
            temperature=0.5
        )
        # Concatenate text from all tokens in all generations
        api_response = ''.join(response)
        return api_response
    except Exception as e:
        return f"Error: {str(e)}"

# Example CSV file path
csv_file_path = 'CARS_2.csv'

# Load dataset from CSV file
dataset = load_dataset_from_csv(csv_file_path)

# Initialize Flask app
app = Flask(__name__)

# Home Page
@app.route("/")
def index():
        return "Hello, World!"

# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['message']
    api_response = generate_api_response(user_input, dataset)
    return jsonify({'response': api_response})

if __name__ == '__main__':
    app.run(debug=True)
