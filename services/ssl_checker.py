from urllib.request import ssl, socket
import validators
from datetime import date, datetime


def get_expiry_dates(hostname):
    # expiry_payload_data
    port = '443'
    context = ssl.create_default_context()
    if validators.domain(hostname):
        try:
            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    dict_data = ssock.getpeercert()
                    # available keys: ['subject', 'issuer', 'version', 'serialNumber', 'notBefore', 'notAfter', 'subjectAltName', 'OCSP', 'caIssuers', 'crlDistributionPoints']
                    start_date = dict_data['notBefore']
                    end_date = dict_data['notAfter']
                    message = True
                    date_today = datetime.today()
                    end_date_to_object = datetime.strptime(end_date, '%b %d %H:%M:%S %Y %Z')
                    if end_date_to_object >= date_today:
                        days_diff = end_date_to_object - date_today
                        days_diff =  days_diff.days
                        expiry_status = "not expired"
                        print(days_diff)
                    else:
                        days_diff = end_date_to_object - date_today
                        days_diff =  days_diff.days
                        expiry_status = "expired"
        except Exception as error:
            message = error
            start_date, end_date = None, None
    else:
        message = "Not valid domain"
        start_date, end_date = None, None
    return message, start_date, end_date