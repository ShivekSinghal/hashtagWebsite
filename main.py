from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, flash, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime  # ⬅️ Add this
import os
import re
import json
import hmac
import hashlib


app = Flask(__name__)

# Razorpay webhook secret - store this securely in environment variables
RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET', 'your_webhook_secret')

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)

CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("Landing Page Registrations").sheet1
SHEET_DROPIN = CLIENT.open("Landing Page Registrations").sheet1

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/openclass")
def main_openclass():
    return render_template("openclass.html")

def is_difference_more_than_2_hours(time_range):
    try:
        start_str, end_str = time_range.split('-')
        start_time = datetime.strptime(start_str, '%H:%M')
        end_time = datetime.strptime(end_str, '%H:%M')

        time_difference = (end_time - start_time).total_seconds() / 3600

        return time_difference > 2
    except ValueError:
        raise ValueError("Time range must be in the format 'HH:MM-HH:MM'")


# Studio to URL mapping
STUDIO_URLS = {
    'Noida': 'https://rzp.io/rzp/oGrCyY3K',
    'Rajouri Garden': 'https://rzp.io/rzp/J5Aal4b4',
    'Pitampura': 'https://rzp.io/rzp/MUOtfB9',
    'Gurgaon': 'https://rzp.io/rzp/ZQmBMw4',
    'East Delhi': 'https://rzp.io/rzp/TQ4ecBN',
    'South Delhi': 'https://rzp.io/rzp/z5WJ4TVU',
    'Indirapuram': 'https://rzp.io/l/pDfeGSjmQ1',
    'Ramgya': 'https://rzp.io/rzp/oGrCyY3K'
}

STUDIO_URLS_DROPIN = {
    'Noida': 'https://rzp.io/rzp/oGrCyY3K',
    'Rajouri Garden': 'https://rzp.io/rzp/J5Aal4b4',
    'Pitampura': 'https://rzp.io/rzp/MUOtfB9',
    'Gurgaon': 'https://rzp.io/rzp/ZQmBMw4',
    'East Delhi': 'https://rzp.io/rzp/3SJEjCS',
    'South Delhi': 'https://rzp.io/rzp/z5WJ4TVU',
    'Indirapuram': 'https://rzp.io/l/pDfeGSjmQ1',
    'Ramgya': 'https://rzp.io/rzp/oGrCyY3K'
}

STUDIO_URLS_PREMIUM_DROPIN = {
    'Noida': 'https://rzp.io/rzp/oGrCyY3K',
    'Rajouri Garden': 'https://rzp.io/rzp/J5Aal4b4',
    'Pitampura': 'https://rzp.io/rzp/MUOtfB9',
    'Gurgaon': 'https://rzp.io/rzp/ZQmBMw4',
    'East Delhi': 'https://rzp.io/rzp/4zBovXMp',
    'South Delhi': 'https://rzp.io/rzp/z5WJ4TVU',
    'Indirapuram': 'https://rzp.io/l/pDfeGSjmQ1',
    'Ramgya': 'https://rzp.io/rzp/oGrCyY3K'
}

STUDIO_URLS_SIXMONTH = {
    'Noida': 'https://rzp.io/rzp/oGrCyY3K',
    'Rajouri Garden': 'https://rzp.io/rzp/J5Aal4b4',
    'Pitampura': 'https://rzp.io/rzp/MUOtfB9',
    'Gurgaon': 'https://rzp.io/rzp/ZQmBMw4',
    'East Delhi': 'https://rzp.io/rzp/TQ4ecBN',
    'South Delhi': 'https://rzp.io/rzp/z5WJ4TVU',
    'Indirapuram': 'https://rzp.io/l/pDfeGSjmQ1',
    'Ramgya': 'https://rzp.io/rzp/oGrCyY3K'
}

STUDIO_URLS_OPENCLASS = {
    'Noida': 'https://rzp.io/rzp/oGrCyY3K',
    'Rajouri Garden': 'https://rzp.io/rzp/J5Aal4b4',
    'Pitampura': 'https://rzp.io/rzp/MUOtfB9',
    'Gurgaon': 'https://rzp.io/rzp/ZQmBMw4',
    'East Delhi': 'https://rzp.io/rzp/TQ4ecBN',
    'South Delhi': 'https://rzp.io/rzp/z5WJ4TVU',
    'Indirapuram': 'https://rzp.io/l/pDfeGSjmQ1',
    'Ramgya': 'https://rzp.io/rzp/oGrCyY3K'
}

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    return render_template('register.html', studios=STUDIO_URLS.keys())

@app.route('/register/process', methods=['POST'])
def register_process():
    try:
        # Get form data
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        studio = request.form.get('studio')
        booking_date = request.form.get('booking_date')
        booking_time = request.form.get('booking_time')
        formatted_date_time = request.form.get('formatted_date_time')

        # Debug logging for time difference
        print(f"Debug - Booking time: {booking_time}")
        is_more_than_2_hours = is_difference_more_than_2_hours(booking_time)
        print(f"Debug - Is more than 2 hours: {is_more_than_2_hours}")
        print(f"Debug - Selected studio: {studio}")

        # Get payment URL based on time difference
        if is_more_than_2_hours:
            payment_url = STUDIO_URLS_PREMIUM_DROPIN.get(studio)
            print(f"Debug - Using PREMIUM_DROPIN URL: {payment_url}")
        else:
            payment_url = STUDIO_URLS_DROPIN.get(studio)
            print(f"Debug - Using regular DROPIN URL: {payment_url}")

        # Log received data
        print(f"Received data: name={name}, phone={phone}, email={email}, studio={studio}, booking_date={booking_date}, booking_time={booking_time}, formatted_date_time={formatted_date_time}")

        # Validate required fields
        if not all([name, phone, email, studio, booking_date, booking_time, formatted_date_time]):
            missing_fields = []
            if not name: missing_fields.append('name')
            if not phone: missing_fields.append('phone')
            if not email: missing_fields.append('email')
            if not studio: missing_fields.append('studio')
            if not booking_date: missing_fields.append('booking_date')
            if not booking_time: missing_fields.append('booking_time')
            if not formatted_date_time: missing_fields.append('formatted_date_time')
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # Validate phone number format
        if not phone.isdigit() or len(phone) != 10:
            return jsonify({'error': 'Invalid phone number format'}), 400

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'error': 'Invalid email format'}), 400

        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Prepare data for Google Sheets
        data = [
            timestamp,  # Timestamp
            name,      # Name
            phone,     # Phone
            email,     # Email
            studio,    # Studio
            formatted_date_time,  # Formatted Date and Time
            booking_time,  # Time Slot
            'Pending'  # Status
        ]

        try:
            # Append data to Google Sheets
            SHEET.append_row(data)
        except Exception as e:
            print(f"Error appending to Google Sheets: {str(e)}")
            return jsonify({'error': 'Failed to save registration data'}), 500

        # Return success response with payment URL
        return jsonify({
            'success': True,
            'payment_url': payment_url
        })

    except Exception as e:
        print(f"Error in register_process: {str(e)}")
        return jsonify({'error': f'An error occurred while processing your registration: {str(e)}'}), 500

@app.route('/registeropenclass', methods=['GET', 'POST'])
def register_openclass():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        studio = request.form.get('studio')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ⬅️ Add this
        print(name, phone, email, studio)
        # Save data to Google Sheet with timestamp
        SHEET.append_row([timestamp, name, phone, email, studio])  # ⬅️ Add timestamp as first colum

        # Optional: Save to DB or do something with the data here

        # Redirect based on selected studio
        redirect_url = STUDIO_URLS_OPENCLASS.get(studio)
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
        print(name, phone, email, studio)
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

@app.route('/booking')
def bookings():
    return render_template("booking.html")

@app.route('/cancel_refund')
def cancel_refund():
    return render_template("cancel_refund.html")

@app.route('/privacypolicy')
def privacypolicy():
    return render_template("privacypolicy.html")

@app.route('/webhook/razorpay', methods=['POST'])
def razorpay_webhook():
    try:
        # Get the webhook signature from headers
        signature = request.headers.get('X-Razorpay-Signature')
        if not signature:
            return jsonify({'error': 'No signature found'}), 400

        # Get the raw request body
        payload = request.get_data()
        
        # Verify webhook signature
        expected_signature = hmac.new(
            RAZORPAY_WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return jsonify({'error': 'Invalid signature'}), 400

        # Parse the webhook payload
        data = request.json
        
        # Check if this is a payment.captured event
        if data.get('event') == 'payment.captured':
            payment = data['payload']['payment']['entity']
            
            # Extract payment details
            payment_id = payment['id']
            amount = payment['amount'] / 100  # Convert from paise to rupees
            currency = payment['currency']
            status = payment['status']
            method = payment['method']
            email = payment['email']
            contact = payment['contact']
            created_at = datetime.fromtimestamp(payment['created_at']).strftime('%Y-%m-%d %H:%M:%S')
            
            # Get additional details from notes
            notes = payment.get('notes', {})
            name = notes.get('name', '')
            customer_email = notes.get('email', '')
            phone = notes.get('phone', '')
            
            # Prepare data for Google Sheets
            row_data = [
                created_at,  # Timestamp
                name,       # Name
                phone,      # Phone
                customer_email,  # Email
                payment_id,  # Payment ID
                f"₹{amount}",  # Amount
                currency,   # Currency
                status,     # Status
                method,     # Payment Method
                'Paid'      # Booking Status
            ]
            
            # Append to Google Sheet
            SHEET_DROPIN.append_row(row_data)
            
            return jsonify({'status': 'success'}), 200
        
        return jsonify({'status': 'ignored'}), 200

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5500)


