import ast
import os
import threading

import ffmpeg
from flask import Blueprint, jsonify, request

from app import db
from models.models import Destination, Stream

app_bp = Blueprint("app", __name__)

# RTMP URL
INPUT_RTMP_URL = os.getenv("INPUT_RTMP_URL")
OUTPUT_RTMP_URL = os.getenv("OUTPUT_RTMP_URL")


def start_restream():
    try:
        (
            ffmpeg.input(INPUT_RTMP_URL)
            .output(
                OUTPUT_RTMP_URL, format="flv", vcodec="copy", acodec="copy"
            )
            .run()
        )
    except Exception as e:
        print(f"An error occurred: {e}")


@app_bp.route("/db", methods=["GET"])
def get_db():
    streams = Stream.query.all()
    stream1_destinations = Destination.query.filter_by(stream_id=1).all()

    return (
        jsonify(
            {
                "message": "DB successfully.",
                "stream1_destinations": str(streams),
                "destinations": str(stream1_destinations),
            }
        ),
        200,
    )


@app_bp.route("/streams", methods=["POST"])
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


@app_bp.route("/streams", methods=["GET"])
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


@app_bp.route("/streams/<stream_name>", methods=["DELETE"])
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


@app_bp.route("/", methods=["GET"])
def start_restream_route():
    threading.Thread(target=start_restream).start()
    return jsonify({"message": "Restreaming started successfully."}), 200
