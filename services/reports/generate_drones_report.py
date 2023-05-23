import json


def generate_drones_json_report(start_date, end_date, data=[], type="on_demand"):
    result = {
        "type": type,
        "date_range": {
            "start_date": start_date,
            "end_date": end_date
        },
        "drones_seen": len(data),
        "drones_count_by_statuses": {
            "hit": len(list(filter(lambda drone: drone.get("status") == "hit", data))),
            "detected": len(list(filter(lambda drone: drone.get("status") == "detected", data))),
            "crushed": len(list(filter(lambda drone: drone.get("status") == "crushed", data))),
            "unknown": len(list(filter(lambda drone: drone.get("status") == "unknown", data))),
        }
    }

    return json.dumps(result)
