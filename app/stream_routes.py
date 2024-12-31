import ast

from flask import Blueprint, jsonify, request

from app import db
from models.models import Stream

stream_bp = Blueprint("stream", __name__)


@stream_bp.route("/streams", methods=["POST"])
def create_stream_route():
    try:
        data = request.get_json()

        if not data:
            return (
                jsonify({"message": "Invalid JSON body provided"}),
                400,
            )

        stream_name = data.get("stream_name")

        if not stream_name:
            return (
                jsonify({"message": "The 'stream_name' field is required"}),
                400,
            )

        if Stream.query.filter_by(stream_name=stream_name).first():
            return (
                jsonify({"message": "The 'stream_name' already exists"}),
                400,
            )

        new_stream = Stream(stream_name=stream_name)

        db.session.add(new_stream)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Stream added successfully!",
                    "stream": {
                        "stream_name": new_stream.stream_name,
                        "streaming_key": new_stream.unique_url,
                    },
                }
            ),
            201,
        )

    except Exception:
        return (jsonify({"message": "An internal server error occurred"}), 500)


@stream_bp.route("/streams", methods=["GET"])
def get_streams():
    streams = Stream.query.all()

    if not streams:
        return (
            jsonify(
                {
                    "message": "No streams available",
                    "streams": {},
                }
            ),
            200,
        )

    return (
        jsonify(
            {
                "message": "Success",
                "streams": {"streams": ast.literal_eval(str(streams))},
            }
        ),
        200,
    )


@stream_bp.route("/streams/<stream_name>", methods=["DELETE"])
def delete_stream(stream_name):
    try:
        stream = Stream.query.filter_by(stream_name=stream_name).first()

        if not stream:
            return (
                jsonify({"message": "The 'stream' does not exist"}),
                400,
            )

        db.session.delete(stream)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Stream deleted successfully!",
                    "stream": {"stream_name": stream_name},
                }
            ),
            200,
        )

    except Exception:
        return (jsonify({"message": "An internal server error occurred"}), 500)
