from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# ===== EMAIL CONFIG =====
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'surfacesolutionalert@gmail.com'        # sender email
app.config['MAIL_PASSWORD'] = 'kdkb nnnp ujwo ggpg'                # use Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = 'surfacesolutionalert@gmail.com'

mail = Mail(app)

# ===== HOME PAGE =====
@app.route("/")
def home():
    return render_template("home.html")

# ===== CONTACT PAGE =====
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        message = request.form["message"]

        msg = Message("New Quote Request",
                      recipients=[
                          "surfacesolutionalert@gmail.com",
                          "5551234567@vtext.com"  # ← replace with your number + carrier
                      ])
        msg.body = (
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Message:\n{message}"
        )

        try:
            mail.send(msg)
            return render_template("contact.html", success=True)
        except Exception as e:
            print(f"Email failed to send: {e}")
            return render_template("contact.html", success=False)

    return render_template("contact.html", success=False)




# ===== SERVICEABILITY CHECKER =====
WACO_ZIPS = {
    "76701", "76704", "76705", "76706", "76707",
    "76708", "76710", "76711", "76712", "76714",
    "76715", "76716", "76797", "76798", "76799"
}

import re

def extract_zip(address):
    match = re.search(r"\b(\d{5})\b", address)
    return match.group(1) if match else None

def is_in_service_area(address):
    zip_code = extract_zip(address)
    return zip_code in WACO_ZIPS if zip_code else False


@app.route("/serviceability", methods=["GET", "POST"])
def serviceability():
    result = None
    if request.method == "POST":
        address = request.form["address"]
        if is_in_service_area(address):
            result = "✅ Good news! We service your area."
        else:
            result = "❌ Sorry, we don’t currently service that address."
    return render_template("serviceability.html", result=result)

# ===== RUN APP =====
if __name__ == "__main__":
    app.run(debug=True)
