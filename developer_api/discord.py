import json
import requests

from flask import url_for
from .settings import config
from .models import Event
import hashlib


def announce_new_event(event):
    email_hash = hashlib.sha256(event.submitor_email.encode()).hexdigest()
    approval_link = url_for('api.approve_event', event_id=event.id, api_key=event.api_key, _external=True)

    request_fields = [{
             "name": "Title",
             "value": event.title
         }, {
             "name": "Description",
             "value": event.description
         }, {
             "name": "Website",
             "value": event.website
         }, {
             "name": "Type",
             "value": event.type.value.title()
         }, {
             "name": "Location",
             "value": f"{event.location_text} ({event.location_longitude}, {event.location_latitude})"
         }, {
             "name": "Start Date",
             "value": f"<t:{event.start_date.timestamp()}:f>"
         }, {
             "name": "End Date",
             "value": f"<t:{event.end_date.timestamp()}:f>"
         }
     ]

    request_data = {
        "embeds": [{
            "author": {
                "icon_url": "https://gravatar.com/avatar/" + email_hash,
                "name": f"{event.submitor_name} <{event.submitor_email}>"
            },
            "title": "New event submitted!",
            "description": f"There's a new event to review. [Approve]({approval_link})",
            "fields": request_fields
        }]
    }

    send_discord_webhook(request_data)

def send_discord_webhook(request_data):
    if config['DISCORD_HOOK_URL'] is not None:
        headers = {'Content-Type': 'application/json'}
        requests.post(config['DISCORD_HOOK_URL'], data=json.dumps(request_data), headers=headers)

