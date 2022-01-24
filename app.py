from urllib import response
from flask import Flask, jsonify, render_template, request
from services.ssl_checker import get_expiry_dates
import re

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template(
            "index.html"
        )
    elif request.method == "POST":
        # Get Form Data
        hostname = request.form['hostname']
        # strip fqdn trimming
        url = re.compile(r"https?://(www\.)?")
        hostname = url.sub('', hostname).strip().strip('/')
        # get expiry data
        expiry_payload_data = get_expiry_dates(hostname)
        if expiry_payload_data["message"] == True:
            return render_template(
                "index_results.html",
                cert_hostname = hostname,
                cert_start_date = expiry_payload_data["start_date"],
                cert_end_date = expiry_payload_data["end_date"],
                cert_expiry_days = expiry_payload_data["days_diff"],
                cert_status = expiry_payload_data["expiry_status"]
            )

        else:
            return render_template(
                "index_results_error.html",
                error_message = expiry_payload_data["message"]
            )
    else:
        return jsonify(
            message="No valid method has been sent"
        )

@app.route('/api/v1/cert_check/check', methods=["GET", "POST"])
def cert_check():
    if request.method == "GET":
        return jsonify(
            # Implement health checker
            health_check="UP"
        )
    elif request.method == "POST":

        hostname = request.json['hostname']
        # strip fqdn trimming
        url = re.compile(r"https?://(www\.)?")
        hostname = url.sub('', hostname).strip().strip('/')
        # get expiry data
        expiry_payload_data = get_expiry_dates(hostname)

        return jsonify(
            cert_hostname = hostname,
            cert_start_date = expiry_payload_data["start_date"],
            cert_end_date = expiry_payload_data["end_date"],
            cert_expiry_days = expiry_payload_data["days_diff"],
            cert_status = expiry_payload_data["expiry_status"]
            
        )
    else:
        return jsonify(
            message="No valid method has been sent"
        )


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")