from app import db


class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash_url = db.Column(db.String(255), unique=True, nullable=False)
    stream_name = db.Column(db.String(255), nullable=False)

    destinations = db.relationship("Destination", backref="stream", lazy=True)

    def __repr__(self):
        return f"<Stream {self.stream_name}>"


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stream_id = db.Column(
        db.Integer, db.ForeignKey("stream.id"), nullable=False
    )
    pid = db.Column(db.Integer, nullable=False)
    dest_url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Destination {self.dest_url}>"
