from urllib.request import ssl, socket
import validators
from datetime import date, datetime


def get_expiry_dates(hostname):
    expiry_payload_data = {
        "start_date":None,
        "end_date":None,
        "message":None,
        "days_diff":None,
        "expiry_status":None
    }
    port = '443'
    context = ssl.create_default_context()
    if validators.domain(hostname):
        try:
            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    dict_data = ssock.getpeercert()
                    # available keys: ['subject', 'issuer', 'version', 'serialNumber', 'notBefore', 'notAfter', 'subjectAltName', 'OCSP', 'caIssuers', 'crlDistributionPoints']
                    expiry_payload_data["start_date"] = dict_data['notBefore']
                    expiry_payload_data["end_date"] = dict_data['notAfter']
                    expiry_payload_data["message"] = True
                    date_today = datetime.today()
                    end_date_to_object = datetime.strptime(expiry_payload_data["end_date"], '%b %d %H:%M:%S %Y %Z')
                    if end_date_to_object >= date_today:
                        days_diff = end_date_to_object - date_today
                        expiry_payload_data["days_diff"] =  days_diff.days
                        expiry_payload_data["expiry_status"] = "not expired"
                    else:
                        days_diff = end_date_to_object - date_today
                        expiry_payload_data["days_diff"] =  days_diff.days
                        expiry_payload_data["expiry_status"] = "expired"
        except Exception as error:
            expiry_payload_data["message"] = error
    else:
        expiry_payload_data["message"] = "Not valid domain"
    return expiry_payload_data