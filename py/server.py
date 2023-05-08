from flask import Flask
import spacy
import json

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.secret_key = "hello_hi"

@app.route('/get/<req>',methods=['GET', 'POST'])
def get(req):
    query = req.replace('+', ' ')
    with open("faqs.json") as faqs_json:
        faqs = json.load(faqs_json)
    doc1 = nlp(query)
    similarity_score = 0
    answer = ''
    for faq in faqs['faqs']:
        print(faq)
        doc2 = nlp(faq['question'])
        score = doc1.similarity(doc2)
        if score > similarity_score:
            answer = faq['answer']
            similarity_score = score
    return(answer)

if __name__ == '__main__':
    app.run(debug=True)