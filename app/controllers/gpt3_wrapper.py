import os
import requests
from settings import BRAIN_OPENAI_URI, GPT3_PROMPT_FILE
from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse

class GPT3Resource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("text", required=True)
    
    def post(self):
        request_data = request.get_json()
        query = request_data.get('text').strip()

        with open(GPT3_PROMPT_FILE, 'r') as f:
            prompt = f.read().replace('\\n', '\n').strip()

        auth_token = os.getenv('BRUS_AUTH_TOKEN')
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"token {auth_token}"
        }

        payload = {
            "prompt": prompt.format(query),
            "max_tokens": 300,
            "temperature": 0.5,
            "engine": "text-curie-001",
            "stop": ['Query', '###']
        }
        response = requests.post(BRAIN_OPENAI_URI, json=payload, headers=headers)
        result = response.json()['choices'][0]['text'].strip()

        return make_response(jsonify(result), 200)
