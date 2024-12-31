import uuid

from app import create_app, db
from models.models import Destination, Stream

app = create_app()


def populate_database():
    with app.app_context():
        if Stream.query.first():
            print("Database already populated.")
            return

        stream1 = Stream(stream_name="Customer 1")
        stream2 = Stream(stream_name="Customer 2")
        stream3 = Stream(stream_name="Customer 3")

        db.session.add_all([stream1, stream2, stream3])
        db.session.commit()

        # Create sample Destination entries
        destinations = [
            Destination(
                stream_id=1,
                pid=20,
                dest_url="rtmp://facebook/static/" + str(uuid.uuid4().hex),
                live="ON",
            ),
            Destination(
                stream_id=1,
                pid=-1,
                dest_url="rtmp://youtube/static/" + str(uuid.uuid4().hex),
                live="OFF",
            ),
            Destination(
                stream_id=1,
                pid=-1,
                dest_url="rtmp://instagram/static/" + str(uuid.uuid4().hex),
                live="OFF",
            ),
            Destination(
                stream_id=2,
                dest_url="rtmp://facebook/static/" + str(uuid.uuid4().hex),
                pid=58,
                live="ON",
            ),
            Destination(
                stream_id=2,
                pid=33,
                dest_url="rtmp://youtube/static/" + str(uuid.uuid4().hex),
                live="ON",
            ),
            Destination(
                stream_id=2,
                pid=24,
                dest_url="rtmp://instagram/static/" + str(uuid.uuid4().hex),
                live="ON",
            ),
        ]

        db.session.add_all(destinations)
        db.session.commit()
        print("Database populated successfully.")


if __name__ == "__main__":
    populate_database()
