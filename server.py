from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
import ssl

def getPassword():
    pass
app_password = getPassword()
sender_email = "jonniketo@gmail.com"

app = Flask(__name__)
CORS(app)

@app.route('/send', methods=['POST'])
def sendEmail():
    data = request.json
    image_data = data['image'].split(",")[1]
    receiver_email = data['email']
    image_bytes = base64.b64decode(image_data)

    subject = "Subject name"
    body = "here is your photo, my dude!"

    image_part = MIMEImage(image_bytes)
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    html_part = MIMEText(body)
    message.attach(html_part)
    message.attach(image_part)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=True, port=5000)
