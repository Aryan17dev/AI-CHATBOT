import os
import time
from flask import Flask, render_template, request
from utils.local_csv import log_to_csv
from utils.local_docs import fill_docx_template
from utils.email_sender import send_email_with_attachment
app = Flask(__name__)

# Track the last time a document was generated to prevent spam
last_submission_time = 0

LOCAL_TEMPLATES = {
    "ip": "doctemplates/IP Template.docx",
    "partnership": "doctemplates/Partnership Template.docx",
    "nda": "doctemplates/NDA Template.docx"
}



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ip-agreement')
def ip_form():
    return render_template('form_ip.html')  # IP Agreement Form

@app.route('/partnership-agreement')
def partnership_form():
    return render_template('form_partnership.html')  # Partnership Agreement Form

@app.route('/nda')
def nda_form():
    return render_template('nda.html')  # Partnership Agreement Form

@app.route('/form/<agreement_type>')
def load_form(agreement_type):
    if agreement_type not in LOCAL_TEMPLATES:
        return "Invalid agreement type", 404
    return render_template(f"form_{agreement_type}.html")

@app.route('/submit/<agreement_type>', methods=["POST"])
def submit(agreement_type):
    global last_submission_time
    
    # Anti-spam logic: Check if 60 seconds have passed since the last submission
    current_time = time.time()
    time_since_last = current_time - last_submission_time
    if time_since_last < 60:
        wait_time = int(60 - time_since_last)
        return f"<h3>To prevent spam, please wait {wait_time} seconds before generating another document.</h3><br><a href='/'>Go back</a>", 429

    if agreement_type not in LOCAL_TEMPLATES:
        return "Invalid agreement type", 404

    template_path = LOCAL_TEMPLATES[agreement_type]
    data = {key: value for key, value in request.form.items()}

    log_to_csv(agreement_type, data)
    docx_path = fill_docx_template(template_path, data)
    
    # Generate a professional subject
    proper_names = {
        "ip": "Intellectual Property Agreement",
        "partnership": "Business Partnership Agreement",
        "nda": "Non-Disclosure Agreement (NDA)"
    }
    document_name = proper_names.get(agreement_type, f"{agreement_type.capitalize()} Agreement")

    send_email_with_attachment(
        to_email=data.get("email"),
        subject=f"Action Required: Your Auto-Generated {document_name}",
        body_text=f"Hello,\n\nPlease find attached your auto-generated {document_name} document. You can open and edit this file in Microsoft Word or Google Docs.\n\nBest regards,\nLegal Documentation Bot",
        filepath=docx_path
    )
    
    if os.path.exists(docx_path):
        os.remove(docx_path)

    # Update the timestamp after successful generation
    last_submission_time = time.time()

    return render_template("success.html", agreement=agreement_type)

if __name__ == "__main__":
    app.run(debug=True)
