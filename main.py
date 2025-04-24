from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, flash, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime  # ⬅️ Add this

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
    'Noida': 'https://rzp.io/l/pDfeGSjmQ1',
    'Rajouri Garden': 'https://rzp.io/l/pDfeGSjmQ1',
    'Pitampura': 'https://rzp.io/l/pDfeGSjmQ1',
    'Gurgaon': 'https://rzp.io/l/pDfeGSjmQ1',
    'East Delhi': 'https://rzp.io/l/pDfeGSjmQ1',
    'South Delhi': 'https://rzp.io/l/pDfeGSjmQ1',
    'Indirapuram': 'https://rzp.io/l/pDfeGSjmQ1',
    'Ramagya': 'https://rzp.io/l/pDfeGSjmQ1'
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



if __name__ == '__main__':
    app.run(debug=True, port=5000)


