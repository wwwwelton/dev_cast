import os
import threading

import ffmpeg
from flask import Blueprint, jsonify

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


@app_bp.route("/", methods=["GET"])
def start_restream_route():
    threading.Thread(target=start_restream).start()
    return jsonify({"message": "Restreaming started successfully."}), 200
