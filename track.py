from google_measurement_protocol import Event, report
import uuid


GENDERS = {
    'female': 'Gender Female',
    'male': 'Gender Male'
}


def log_fetch(count, gender):
    label = GENDERS.get(gender, 'Gender Neutral')
    client_id = uuid.uuid4()
    event = Event('API', 'Fetch', label=label, value=count)
    report('UA-68765997-3', client_id, event)
