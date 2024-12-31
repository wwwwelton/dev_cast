from app import create_app, db
from models.models import Destination, Stream

app = create_app()


def populate_database():
    with app.app_context():
        if Stream.query.first():
            print("Database already populated.")
            return

        stream1 = Stream(hash_url="a1b2c3d", stream_name="Customer 1")
        stream2 = Stream(hash_url="f7g8h9i", stream_name="Customer 2")
        stream3 = Stream(hash_url="z9y8x7w", stream_name="Customer 3")

        db.session.add_all([stream1, stream2, stream3])
        db.session.commit()

        # Create sample Destination entries
        destinations = [
            Destination(
                stream_id=1, pid=20, dest_url="DEST 1 URL", status="ON"
            ),
            Destination(
                stream_id=1, pid=-1, dest_url="DEST 2 URL", status="OFF"
            ),
            Destination(
                stream_id=1, pid=-1, dest_url="DEST 3 URL", status="OFF"
            ),
            Destination(
                stream_id=2, pid=58, dest_url="DEST 1 URL", status="ON"
            ),
            Destination(
                stream_id=2, pid=33, dest_url="DEST 2 URL", status="ON"
            ),
            Destination(
                stream_id=2, pid=24, dest_url="DEST 3 URL", status="ON"
            ),
        ]

        db.session.add_all(destinations)
        db.session.commit()
        print("Database populated successfully.")


if __name__ == "__main__":
    populate_database()
