import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from flask import Flask, request, jsonify
from waitress import serve

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Medical Diagnostic Chatbot!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_input = data['input_text']

    # Generate response using the model
    input_ids = tokenizer.encode(user_input, return_tensors='pt')
    response_ids = model.generate(input_ids, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    response_text = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    
    return jsonify({'response': response_text})

# def create_app():
#    return app
if __name__ == '__main__':
    app.run(debug=True)
    # serve(app, host="0.0.0.0", port=8080)
    


