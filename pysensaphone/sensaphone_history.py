def device_history(device_id, zone_ids):
    """Get history of data log of a device"""

    # need to get log point then get history for log point....
    # log_points is an array...

    global account_id, session
    url = "https://rest.sensaphone.net/api/v1/history/data_log_points"

    payload = {
        "request_type": "read",
        "acctid": account_id,
        "session": session,
        "history":
            {
                "data_log_points": {
                    "resource_type": "device",
                    "device_id": device_id
                }
            }
    }

    data = sensaphone_request(url, payload)
    log_points = []
    for z in data['response']['history']['data_log_points']['log_points']:
        if z['zone_id'] in zone_ids:
            log_points.append(z['log_point'])

    # print(json.dumps(data))
    # exit(0)

    ts = sensaphone_timestamp(10)

    url = "https://rest.sensaphone.net/api/v1/history/data_log"

    payload = {
        "request_type": "read",
        "acctid": account_id,
        "session": session,
        "history":
            {
                "data_log": {
                    "log_points": log_points,
                    "start": ts
                }
            }
    }

    data = sensaphone_request(url, payload)
    print(json.dumps(data))
    exit(0)
    return data


def sensaphone_timestamp(hours):
    delta = datetime.datetime.utcnow() - datetime.timedelta(hours=hours)
    print(delta)

    ts = (delta.second % 60) + ((delta.minute * 60) % 3600) + ((delta.hour * 3600) % 86400) + (
                (delta.day * 86400) % 2678400) + ((delta.month * 2678400) % 32140800) + ((delta.year % 100 * 32140800))
    print(ts)
    return ts