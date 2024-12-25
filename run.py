from flask import Flask, jsonify
import ffmpeg
import threading

app = Flask(__name__)

INPUT_RTMP_URL = "rtmp://XXXXX"
OUTPUT_RTMP_URL = "rtmp://XXXXX"


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


@app.route("/", methods=["GET"])
def start_restream_route():
    threading.Thread(target=start_restream).start()
    return jsonify({"message": "Restreaming started successfully."}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
