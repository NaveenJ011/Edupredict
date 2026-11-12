
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict_performance

app = Flask(__name__)
CORS(app)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "EduPredict backend is running!"
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        attendance = float(data["attendance"])
        study_hours = float(data["study_hours"])
        previous_marks = float(data["previous_marks"])
        assignment_marks = float(data["assignment_marks"])

        if not 0 <= attendance <= 100:
            return jsonify({"error": "Attendance must be between 0 and 100"}), 400

        if not 0 <= study_hours <= 24:
            return jsonify({"error": "Study hours must be between 0 and 24"}), 400

        if not 0 <= previous_marks <= 100:
            return jsonify({"error": "Previous marks must be between 0 and 100"}), 400

        if not 0 <= assignment_marks <= 100:
            return jsonify({"error": "Assignment marks must be between 0 and 100"}), 400

        result = predict_performance(
            attendance,
            study_hours,
            previous_marks,
            assignment_marks
        )

        return jsonify(result)

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Please provide valid student details."
        }), 400


if __name__ == "__main__":
    app.run(debug=True)
