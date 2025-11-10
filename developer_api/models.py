import secrets

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func
from enum import Enum
from .utils import geolocate, parse_date


class EventType(Enum):
    HACKATHON = 'hackathon'
    MEETUP = 'meetup'
    PARTY = 'party'
    OTHER = 'other'

db = SQLAlchemy()
migrate = Migrate()

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(64), nullable=False)
    type = db.Column(db.Enum(EventType), nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    all_day = db.Column(db.Boolean, nullable=False)
    submitor_email = db.Column(db.String(64), nullable=False)
    submitor_name = db.Column(db.String(64), nullable=False)
    location_text = db.Column(db.String(64), nullable=False)
    location_longitude = db.Column(db.Float)
    location_latitude = db.Column(db.Float)
    approved = db.Column(db.Boolean, nullable=False, default=False)
    api_key = db.Column(db.String(64), nullable=False)

    @classmethod
    def from_json(cls, event_json):
        try:
            event = cls(
                title=event_json['title'],
                description=event_json['description'],
                website=event_json['website'],
                type=EventType[event_json['type'].upper()],
                end_date=parse_date(event_json['endDate']),
                start_date=parse_date(event_json['startDate']),
                all_day=event_json['isAllDay'].lower() == 'true',
                location_text=event_json['location[text]'],
                submitor_email=event_json['submission[email]'],
                submitor_name=event_json['submission[name]'],
                api_key=secrets.token_urlsafe(32),
            )
            event.location_longitude, event.location_latitude = geolocate(event.location_text)
            return event
        except (KeyError, ValueError):
            return None

    def to_json(self):
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'website': self.website,
            'type': self.type.value.title(),
            'endDate': self.end_date,
            'startDate': self.start_date,
            'location': self.location_text,
            'longitude': self.location_longitude,
            'latitude': self.location_latitude
        }

        return result

def init_app(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

