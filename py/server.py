from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask
import spacy
import json
import smtplib

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.secret_key = "hello_hi"

sender_email = "reviewgagteam@gmail.com"
sender_password = "arnav00782"
receiver_email = "devesh97531@gmail.com"
subject = "Chatbot Question"

def send_email(sender_email, sender_password, receiver_email, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return "Email sent successfully!"
    except Exception as e:
        return "An error occurred while sending the email:", str(e)

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
        if score > similarity_score and score > 0.2:
            answer = faq['answer']
            similarity_score = score
        elif score <= 0.2:
            send_email(sender_email,sender_password,receiver_email,subject,query)
    return(answer)


@app.route('/send/<req>',methods=['GET', 'POST'])
def send(req):
    query = req.replace('+', ' ')
    return send_email(sender_email,sender_password,receiver_email,subject,query)

if __name__ == '__main__':
    app.run(debug=True)