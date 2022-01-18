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
        message, start_date, end_date = get_expiry_dates(hostname)
        if message == True:
            return render_template(
                "index_results.html",
                cert_hostname = hostname,
                cert_start_date = start_date,
                cert_end_date = end_date
            )

        else:
            return render_template(
                "index_results_error.html",
                cert_hostname = hostname,
                cert_start_date = start_date,
                cert_end_date = end_date,
                error_message = message
            )
    else:
        return jsonify(
            message="No valid method has been sent"
        )

@app.route('/api/v1/cert_check/<string:hostname>', methods=["GET", "POST"])
def cert_check(hostname):
    if request.method == "GET":
        return jsonify(
            health_check="UP"
        )
    elif request.method == "POST":
        # strip fqdn trimming
        url = re.compile(r"https?://(www\.)?")
        hostname = url.sub('', hostname).strip().strip('/')
        # get expiry data
        message, start_date, end_date = get_expiry_dates(hostname)

        return jsonify(
            response="not expired"
            
        )
    else:
        return jsonify(
            message="No valid method has been sent"
        )


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")