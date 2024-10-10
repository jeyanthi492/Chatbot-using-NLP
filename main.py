from flask import Flask, render_template, request
import random
import pandas as pd

app = Flask(__name__)

# Load intents and responses from an Excel file
def load_intents_from_excel(file_path):
    intents_df = pd.read_excel(file_path)
    intents = {}
    for index, row in intents_df.iterrows():
        intent = row['Intent']

        if intent not in intents:
            intents[intent] = {"patterns": [], "responses": []}
        intents[intent]["patterns"].append(row['Pattern'])
        intents[intent]["responses"].append(row['Response'])
    return intents

# Function to find the intent of user input
def find_intent(user_input):
    for intent, data in intents.items():
        for pattern in data["patterns"]:
            if pattern in user_input:
                return intent
    return None

# Function to generate response based on the intent
def generate_response(intent):
    if intent in intents:
        responses = intents[intent]["responses"]
        return random.choice(responses)
    return "I'm not sure how to respond to that."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input'].lower()
    intent = find_intent(user_input)
    response = generate_response(intent)
    return response

# Load intents from Excel file
intents = load_intents_from_excel("intents.xlsx")

if __name__ == '__main__':
    app.run(debug=True)