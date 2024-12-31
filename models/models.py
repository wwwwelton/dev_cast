import ast
import uuid

from app import db


class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stream_key = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4().hex),
    )
    stream_name = db.Column(db.String(255), nullable=False)
    live = db.Column(db.String(10), nullable=False, default="OFF")

    destinations = db.relationship(
        "Destination",
        backref="stream",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, stream_name):
        self.stream_name = stream_name

    def __repr__(self):
        return str(
            {
                "stream_name": self.stream_name,
                "stream_key": self.stream_key,
                "live": self.live,
                "destinations": ast.literal_eval(str(self.destinations)),
            }
        )


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stream_id = db.Column(
        db.Integer, db.ForeignKey("stream.id"), nullable=False
    )
    pid = db.Column(db.Integer, nullable=False, default=-1)
    dest_name = db.Column(db.String(255), nullable=False)
    dest_url = db.Column(db.String(255), nullable=False)
    live = db.Column(db.String(10), nullable=False, default="OFF")

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "dest_name": self.dest_name,
                "dest_url": self.dest_url,
                "live": self.live,
            }
        )
