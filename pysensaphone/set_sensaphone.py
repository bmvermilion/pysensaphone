from .get_sensaphone import sensaphone_request


def change_device_output(creds, device_id, zone_id, pump_value):

    url = "https://rest.sensaphone.net/api/v1/device/zone"
    payload = {
        "request_type": "update",
        "resource": "device",
        "acctid": creds['acctid'],
        "session": creds['session'],
        "device": [
            {
                "device_id": device_id,
                "zone": [
                    {
                        "zone_id": zone_id,
                        "output_zone": {
                                "value": pump_value
                            }
                    }
                ]
            }
        ]
    }

    data = sensaphone_request(url, payload)

    return data
