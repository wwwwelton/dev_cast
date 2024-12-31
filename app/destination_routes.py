import ast

from flask import Blueprint, jsonify, request

from app import db
from models.models import Destination, Stream

destination_bp = Blueprint("destination", __name__)


@destination_bp.route("/destinations", methods=["POST"])
def create_destination():
    try:
        data = request.get_json()

        if not data:
            return (
                jsonify({"message": "Invalid JSON body provided"}),
                400,
            )

        stream_key = data.get("stream_key")
        dest_name = data.get("dest_name")
        dest_url = data.get("dest_url")

        if not stream_key or not dest_name or not dest_url:
            return (
                jsonify(
                    {
                        "message": (
                            "The 'stream_key', 'dest_name' and 'dest_url' "
                            "fields are required"
                        )
                    }
                ),
                400,
            )

        result = (
            Stream.query.join(Destination)
            .filter(
                Stream.stream_key == stream_key,
                Destination.dest_name == dest_name,
            )
            .first()
        )

        if result:
            return (
                jsonify({"message": "The 'dest_name' already exists"}),
                400,
            )

        stream = Stream.query.filter_by(stream_key=stream_key).first()
        new_dest = Destination(
            stream=stream,
            dest_name=dest_name,
            dest_url=dest_url,
        )

        db.session.add(new_dest)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Destination added successfully!",
                    "destination": {
                        "stream_name": stream.stream_name,
                        "stream_key": stream.stream_key,
                        "dest_name": new_dest.dest_name,
                        "dest_url": new_dest.dest_url,
                    },
                }
            ),
            201,
        )

    except Exception:
        return (jsonify({"message": "An internal server error occurred"}), 500)


@destination_bp.route("/destinations/<stream_key>", methods=["GET"])
def get_destinations(stream_key):
    try:
        stream = Stream.query.filter_by(stream_key=stream_key).first()

        if not stream:
            return (
                jsonify(
                    {
                        "message": "The 'stream_key' does not exist",
                        "destination": {},
                    }
                ),
                400,
            )

        if "id" in request.args:
            id = request.args.get("id")
            return get_destination(stream_key=stream_key, id=id)

        destinations = stream.destinations

        if not destinations:
            return (
                jsonify(
                    {
                        "message": "No destinations available",
                        "destinations": {},
                    }
                ),
                200,
            )

        return (
            jsonify(
                {
                    "message": "Success",
                    "destinations": ast.literal_eval(str(destinations)),
                }
            ),
            200,
        )
    except Exception:
        return (jsonify({"message": "An internal server error occurred"}), 500)


# @destination_bp.route("/destinations/<stream_key>/<id>", methods=["GET"])
def get_destination(stream_key, id):
    try:
        stream = Stream.query.filter_by(stream_key=stream_key).first()

        if not stream:
            return (
                jsonify(
                    {
                        "message": "The 'stream_key' does not exist",
                        "destination": {},
                    }
                ),
                400,
            )

        destination = [
            dest for dest in stream.destinations if dest.id == int(id)
        ]

        if not destination:
            return (
                jsonify(
                    {
                        "message": "The 'id' does not exist",
                        "destination": {},
                    }
                ),
                200,
            )

        return (
            jsonify(
                {
                    "message": "Success",
                    "destination": ast.literal_eval(str(destination[0])),
                }
            ),
            200,
        )
    except Exception:
        return (jsonify({"message": "An internal server error occurred"}), 500)
