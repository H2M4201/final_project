import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


def emotion_detector(text_to_analyze):
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=input_json
    )

    result = response.json()

    emotions = result["emotionPredictions"][0]["emotion"]

    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
        "dominant_emotion": dominant_emotion
    }


@app.route("/", methods=["GET"])
def emotion_detection():
    text_to_analyze = request.args.get("text_to_analyze")

    result = emotion_detector(text_to_analyze)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)