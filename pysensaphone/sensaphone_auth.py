import boto3
import os
import datetime
import json
from base64 import b64decode
from pathlib import Path
from .get_sensaphone import sensaphone_request


def sensaphone_login():
    """
    Login to Sensaphone and collect session, acctid and session_expiration
    """
    username = 'controls@melodywoods.awsapps.com'
    password = decrypt_password()
    login_data = {"request_type": "create", "resource": "login", "user_name": username, "password": password}
    url = 'https://rest.sensaphone.net/api/v1/login'

    print('Attempting to Login to Sensaphone')
    r = sensaphone_request(url, login_data)

    if r['result']['success']:
        creds = {'session': r['response']['session'], 'acctid': r['response']['acctid'], 'session_expiration': str(
            datetime.datetime.fromtimestamp(r['response']['session_expiration'] + r['response']['login_timestamp']))}
        if os.environ.get("AWS_EXECUTION_ENV"):
            pass
        else:
            with open('creds.json', 'w') as fp:
                json.dump(creds, fp)
        print('Auth Success')
        return creds
    else:
        print('Auth Failure Sensaphone Account ', r['result'])
        return False


def check_valid_session():
    """
    Check if current session id is valid. If not then login
    """
    if os.environ.get("AWS_EXECUTION_ENV"):
        sensaphone_login()
    else:
        try:
            with open('creds.json', 'r') as fp:
                creds = json.load(fp)
        except FileNotFoundError:
            return sensaphone_login()
        else:
            session_expiration = datetime.datetime.strptime(creds['session_expiration'], '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()
            time_till_expire = session_expiration - now

            if time_till_expire.total_seconds() / 3660 > 1.0:
                return creds
            else:
                print("Sensaphone Creds Expired")
                return sensaphone_login()


def decrypt_password():

    path = Path(__file__).parent / "encrypted_controls.pem"
    with open(path, 'r') as encrypted_pem:
        pem_file = encrypted_pem.read()

    kms = boto3.client('kms', region_name='us-west-2')
    return kms.decrypt(CiphertextBlob=b64decode(pem_file))['Plaintext'].decode("utf-8")