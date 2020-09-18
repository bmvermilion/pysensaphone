import boto3
import os
import datetime
import json
from base64 import b64decode
from pathlib import Path
from .get_sensaphone import sensaphone_request


def sensaphone_login() -> dict:
    """Login to Sensaphone and collect session, acctid and session_expiration

    Parameters
    ----------

    Returns
    -------
    dict
        returns dictionary with session, account id and expiration timestamp,
            for use with authentication with Sensaphone API.

    TODO
    -------
    Cache credential in AWS for retrieval and use if they are still valid.
        To prevent having to login for every Lambda function run.
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
            # TODO - Cache valid credentials in AWS
            pass
        else:
            with open('creds.json', 'w') as fp:
                json.dump(creds, fp)
        print('Auth Success')
        return creds
    else:
        print('Auth Failure Sensaphone Account ', json.dumps(r))
        return False


def check_valid_session() -> dict:
    """Check if current session id is valid. If not then login using sensaphone_login()

    Parameters
    ----------

    Returns
    -------
    dict
        returns dictionary with session, account id and expiration timestamp,
            for use with authentication with Sensaphone API.
    """

    if os.environ.get("AWS_EXECUTION_ENV"):
        # TODO - Read from cache of valid credentials in AWS
        return sensaphone_login()
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
                print("Sensaphone Credentials Expired")
                return sensaphone_login()


def decrypt_password() -> str:
    """Decrypt password stored in .pem file using AWS Key Management Service (KMS).

    Parameters
    ----------

    Returns
    -------
        str
            returns password as string for use in authentication with Sensaphone.
        """

    path = Path(__file__).parent / "encrypted_controls.pem"
    with open(path, 'r') as encrypted_pem:
        pem_file = encrypted_pem.read()

    kms = boto3.client('kms', region_name='us-west-2')
    return kms.decrypt(CiphertextBlob=b64decode(pem_file))['Plaintext'].decode("utf-8")