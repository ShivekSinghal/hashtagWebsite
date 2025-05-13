from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, flash, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime  # ⬅️ Add this
import os
app = Flask(__name__)

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)

CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("Landing Page Registrations").sheet1

@app.route("/")
def main():
    return render_template("index.html")

# Studio to URL mapping
STUDIO_URLS = {
    'Noida': 'https://rzp.io/rzp/oGrCyY3K',
    'Rajouri Garden': 'https://rzp.io/rzp/J5Aal4b4',
    'Pitampura': 'https://rzp.io/rzp/MUOtfB9',
    'Gurgaon': 'https://rzp.io/rzp/ZQmBMw4',
    'East Delhi': 'https://rzp.io/rzp/TQ4ecBN',
    'South Delhi': 'https://rzp.io/rzp/z5WJ4TVU',
    'Indirapuram': 'https://rzp.io/l/pDfeGSjmQ1',
    'Ramagya': 'https://rzp.io/rzp/oGrCyY3K'
}

STUDIO_URLS_DROPIN = {
    'Noida': 'https://rzp.io/rzp/oGrCyY3K',
    'Rajouri Garden': 'https://rzp.io/rzp/J5Aal4b4',
    'Pitampura': 'https://rzp.io/rzp/MUOtfB9',
    'Gurgaon': 'https://rzp.io/rzp/ZQmBMw4',
    'East Delhi': 'https://rzp.io/rzp/TQ4ecBN',
    'South Delhi': 'https://rzp.io/rzp/z5WJ4TVU',
    'Indirapuram': 'https://rzp.io/l/pDfeGSjmQ1',
    'Ramagya': 'https://rzp.io/rzp/oGrCyY3K'
}

STUDIO_URLS_SIXMONTH= {
    'Noida': 'https://rzp.io/rzp/oGrCyY3K',
    'Rajouri Garden': 'https://rzp.io/rzp/J5Aal4b4',
    'Pitampura': 'https://rzp.io/rzp/MUOtfB9',
    'Gurgaon': 'https://rzp.io/rzp/ZQmBMw4',
    'East Delhi': 'https://rzp.io/rzp/TQ4ecBN',
    'South Delhi': 'https://rzp.io/rzp/z5WJ4TVU',
    'Indirapuram': 'https://rzp.io/l/pDfeGSjmQ1',
    'Ramagya': 'https://rzp.io/rzp/oGrCyY3K'
}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        studio = request.form.get('studio')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ⬅️ Add this

        # Save data to Google Sheet with timestamp
        SHEET.append_row([timestamp, name, phone, email, studio])  # ⬅️ Add timestamp as first column

        # Optional: Save to DB or do something with the data here

        # Redirect based on selected studio
        redirect_url = STUDIO_URLS.get(studio)
        if redirect_url:
            return redirect(redirect_url)
        else:
            return "Invalid studio selected", 400

    return render_template('register.html', studios=STUDIO_URLS.keys())



@app.route('/register_sixmonths', methods=['GET', 'POST'])
def register_hashtag():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        studio = request.form.get('studio')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ⬅️ Add this

        # Save data to Google Sheet with timestamp
        SHEET.append_row([timestamp, name, phone, email, studio])  # ⬅️ Add timestamp as first column

        # Optional: Save to DB or do something with the data here

        # Redirect based on selected studio
        redirect_url = STUDIO_URLS_SIXMONTH.get(studio)
        if redirect_url:
            return redirect(redirect_url)
        else:
            return "Invalid studio selected", 400

    return render_template('register.html', studios=STUDIO_URLS.keys())

@app.route('/terms')
def terms_and_conditions():
    return render_template("terms.html")

@app.route('/privacypolicy')
def privacypolicy():
    return render_template("privacypolicy.html")


if __name__ == '__main__':
    app.run(debug=True, port=5500)


