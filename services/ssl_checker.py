from urllib.request import ssl, socket
import validators
from datetime import date   


def get_expiry_dates(hostname):
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
        except Exception as error:
            message = error
            start_date, end_date = None, None
    else:
        message = "Not valid domain"
        start_date, end_date = None, None
    return message, start_date, end_date