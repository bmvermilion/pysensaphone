import requests
from requests.exceptions import HTTPError
import json
from urllib.parse import urlparse


def sensaphone_request(url, data):
    """
    General Sensaphone Sentinel Request
    """
    try:
        response = requests.post(url=url, data=json.dumps(data))
        r = json.loads(response.text)

        if r['result']['success']:
            print('API Request Success! ' + urlparse(url).path)
            return r
        else:
            if r['result']['code'] == 2:
                print('Session Expired! How?', r)
                return False
            else:
                print(r)
                return False

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_all_device_id(creds):
    """
    Get all if of devices connected to account
    """

    url = 'https://rest.sensaphone.net/api/v1/device'
    payload = {
        "request_type": "read",
        "resource": "device",
        "acctid": creds['acctid'],
        "session": creds['session'],
        "device": None
    }

    data = sensaphone_request(url, payload)
    print(json.dumps(data))
    devices = []
    for d in data['response']['device']:
        sensors = []
        for z in d['zone']:
            if z['enable']:
                sensors.append(
                    {"name": z['name'], "zone_id": z['zone_id'], "sensor_type": z['type'], "units": z['units'],
                     "value": z['value']})
        devices.append(
            {"name": d['name'], "device_id": d['device_id'], "description": d['description'], "zone": sensors})

    return devices


def device_info(creds, device_id):
    """
    Get information about specific devices
    """

    url = 'https://rest.sensaphone.net/api/v1/device'
    payload = {
        "request_type": "read",
        "resource": "device",
        "acctid": creds['acctid'],
        "session": creds['session'],
        "device": [
            {
                "device_id": device_id
            }
        ]
    }

    data = sensaphone_request(url, payload)

    devices = []
    for d in data['response']['device']:
        sensors = []
        for z in d['zone']:
            if z['enable']:
                sensors.append(
                    {"name": z['name'], "zone_id": z['zone_id'], "sensor_type": z['type'], "units": z['units'],
                     "value": z['value']})
        devices.append(
            {"name": d['name'], "device_id": d['device_id'], "description": d['description'], "zone": sensors})

    return devices


def device_sensor_info(creds, device_id, zone_id):
    """
    Get information about a specific sensor on a device
    """

    url = "https://rest.sensaphone.net/api/v1/device/zone"
    payload = {
        "request_type": "read",
        "resource": "device",
        "acctid": creds['acctid'],
        "session": creds['session'],
        "device": [
            {
                "device_id": device_id,
                "zone": [
                    {
                        "zone_id": zone_id
                    }
                ]
            }
        ]
    }

    data = sensaphone_request(url, payload)

    return data






