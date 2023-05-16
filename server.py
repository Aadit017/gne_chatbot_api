from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy
import json
import smtplib

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.secret_key = "hello_hi"
CORS(app)

sender_email = "chatbot_gne@yahoo.com"
sender_password = "GNDEC-chat"
receiver_email = "devesh97531@gmail.com"
subject = "Chatbot Question"

def send_email(sender_email, sender_password, receiver_email, subject, message):
    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        # Create a secure SSL/TLS connection with the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            # Login to the Gmail account
            server.login(sender_email, sender_password)
            # Send the email
            server.send_message(msg)
        print("Email sent successfully!")
        return "Email sent successfully!"
    except Exception as e:
        print("An error occurred while sending the email:" + str(e))
        return "An error occurred while sending the email:" + str(e)

@app.route('/query',methods=['POST'])
def get():
    query = request.get_json()['query'];
    with open("faqs.json") as faqs_json:
        faqs = json.load(faqs_json)
    doc1 = nlp(query)
    similarity_score = 0
    answer = ''
    for faq in faqs['faqs']:
        doc2 = nlp(faq['question'])
        score = doc1.similarity(doc2)
        if score > similarity_score:
            answer = faq['answer']
            similarity_score = score
    if similarity_score <= 0.2:
        return send_email(sender_email,sender_password,receiver_email,subject,query), 200
    return answer, 200


@app.route('/get-all')
def get_all():
    with open("faqs.json") as faqs_json:
        faqs = json.load(faqs_json)
    return jsonify(faqs)

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

@app.route('/send/<req>',methods=['GET', 'POST'])
def send(req):
    query = req.replace('+', ' ')
    return send_email(sender_email,sender_password,receiver_email,subject,query)

if __name__ == '__main__':
    app.run(debug=True)
