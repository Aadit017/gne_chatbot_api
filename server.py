from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, jsonify
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

    smtp =  smtplib.SMTP(smtp_server, smtp_port)
    print("loggin in");
    smtp.starttls()
    print("started tls");
    smtp.login(sender_email, sender_password)
    print("logged in");
    smtp.send_email(msg)
    smtp.quit()
    return "Email sent successfully!"

@app.route('/get/<req>',methods=['GET', 'POST'])
def get(req):
    query = req.replace('+', ' ')
    with open("faqs.json") as faqs_json:
        faqs = json.load(faqs_json)
    doc1 = nlp(query)
    similarity_score = 0
    answer = ''
    for faq in faqs['faqs'].values():
        doc2 = nlp(faq['question'])
        score = doc1.similarity(doc2)
        if score > similarity_score and score > 0.2:
            answer = faq['answer']
            similarity_score = score
        elif score <= 0.2:
            send_email(sender_email,sender_password,receiver_email,subject,query)
    return(answer)


@app.route('/get-all')
def get_all():
    with open("faqs.json") as faqs_json:
        faqs = json.load(faqs_json)
    return jsonify(faqs)

@app.route('/send/<req>',methods=['GET', 'POST'])
def send(req):
    query = req.replace('+', ' ')
    return send_email(sender_email,sender_password,receiver_email,subject,query)

if __name__ == '__main__':
    app.run(debug=True)
