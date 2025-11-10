from flask import Blueprint, jsonify, request, current_app
from flask_cors import cross_origin
import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from .models import db, Event
from .utils import api_error
from .settings import config
from .discord import announce_new_event

import beeline

api = Blueprint('api', __name__)

@api.route('/events/submit', methods=['POST'])
@api.route('/events/submit.json', methods=['POST'])
def submit_event():
    try:
        event_json = request.form
        event = Event.from_json(event_json)
    except ValueError:
        return api_error(400)

    db.session.add(event)
    db.session.commit()

    announce_new_event(event)

    result = {
        'message': 'Thank you for the submission!'
    }

    return jsonify(result)


@api.route('/events/approve/<event_id>')
def approve_event(event_id):
    api_key = request.args.get('api_key')
    if not api_key:
        abort(401)

    event = Event.query.filter_by(id=event_id, api_key=api_key).one_or_none()

    if not event:
        abort(404)

    event.approved = True
    db.session.add(event)
    db.session.commit()

    return 'OK'


@api.route('/events/locations')
@api.route('/events/locations.json')
@cross_origin()
def locations():
    # I'm not aware of any significant locations for the Pebble Community
    return jsonify([])


@api.route('/events/upcoming')
@api.route('/events/upcoming.json')
@cross_origin()
def upcoming_events():
    try:
        limit = int(request.args.get('limit', 60))
        start_date = datetime.strptime(request.args.get('start', date.today().strftime("%Y/%m/%d")), "%Y/%m/%d")
        end_date = datetime.strptime(request.args.get('end', (date.today() + relativedelta(months=6)).strftime("%Y/%m/%d")), "%Y/%m/%d")
    except ValueError:
        return api_error(410)

    events = Event.query.filter(Event.start_date <= end_date, Event.end_date >= start_date, Event.approved == True)
    return jsonify([event.to_json() for event in events.order_by(Event.start_date.asc())])


@api.errorhandler(404)
def page_not_found(e):
    return api_error(404)


@api.errorhandler(500)
def internal_server_error(e):
    return api_error(500)


def init_api(app, url_prefix=''):
    app.register_blueprint(api, url_prefix=url_prefix)
