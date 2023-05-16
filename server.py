from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy
import json

nlp = spacy.load("en_core_web_md")

app = Flask(__name__)
app.secret_key = "hello_hi"
CORS(app)

threshold_similarity = 0.7

def calculate_similarity(query, text):
    query_doc = nlp(query)
    text_doc = nlp(text)

    similarity_scores = []
    for query_token in query_doc:
        max_similarity = max(query_token.similarity(text_token) for text_token in text_doc)
        similarity_scores.append(max_similarity)

    avg_similarity = sum(similarity_scores) / len(similarity_scores)
    return avg_similarity

@app.route('/query', methods=['POST'])
def get():
    query = request.get_json()['query']
    
    with open("faqs.json") as faqs_json:
        faqs = json.load(faqs_json)
    
    doc1 = nlp(query)
    response = []
    
    for faq in faqs['faqs']:
        question = faq['question']
        similarity_score = calculate_similarity(query, question)
        
        if similarity_score > threshold_similarity:
            response.append({"question": question, "answer": faq['answer'], "similarity_score": similarity_score})
    
    if len(response) == 0:
        with open("queries.json", "r") as queries_json:
            queries = json.load(queries_json)
        
        with open("queries.json", "w") as queries_json:
            queries['queries'].append({'question': query})
            json.dump(queries, queries_json, indent=4)
        
        response.append({"question": query, "answer": "Couldn't find the answer to that question, but don't worry. We'll be replying back with the appropriate information as soon as possible.", "similarity_score": 0.0})
    else:
        response = sorted(response, key=lambda x: x["similarity_score"], reverse=True)
    
    return jsonify(response), 200

@app.route('/get-all')
def get_all():
    with open("faqs.json") as faqs_json:
        faqs = json.load(faqs_json)
    return jsonify(faqs)

@app.route('/get-queries')
def get_queries():
    with open("queries.json") as queries_json:
        queries = json.load(queries_json)
    return jsonify(queries)

@app.route('/remove-query', methods=['POST'])
def remove_query():
    json_data = request.get_json()
    with open("queries.json", "r") as queries_json:
        queries = json.load(queries_json)

    index_to_delete = int(json_data['index'])
    if index_to_delete is not None:
        del queries['queries'][index_to_delete]

    with open("queries.json", "w") as queries_json:
        json.dump(queries, queries_json, indent=4)

    return "removed successfully", 200

@app.route('/add',methods=['POST'])
def add():    
    json_data = request.get_json()
    with open("faqs.json","r") as faqs_json:
        faqs = json.load(faqs_json)
    with open("faqs.json","w") as faqs_json:
        faqs['faqs'].append({'question':json_data['question'],'answer':json_data['answer']})
        json.dump(faqs, faqs_json, indent=4)
    return "Added successfully"

@app.route('/remove', methods=['POST'])
def remove():
    json_data = request.get_json()
    with open("faqs.json", "r") as faqs_json:
        faqs = json.load(faqs_json)

    index_to_delete = int(json_data['index'])
    if index_to_delete is not None:
        del faqs['faqs'][index_to_delete]

    with open("faqs.json", "w") as faqs_json:
        json.dump(faqs, faqs_json, indent=4)

    return "removed successfully", 200

if __name__ == '__main__':
    app.run(debug=True)
