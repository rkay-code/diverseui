from google_measurement_protocol import Event, report
import uuid


def log_fetch(count, gender):
    gender = "Gender %s" % gender
    client_id = uuid.uuid4()
    event = Event('API', 'Fetch', label=gender, value=count)
    report('UA-68765997-3', client_id, event)
