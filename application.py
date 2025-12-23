import joblib
import os
import numpy as np
from flask import Flask, render_template, request
from config.paths_config import MODEL_OUTPUT_PATH

app = Flask(__name__)

# Global variable (initially empty)
loaded_model = None

def get_model():
    global loaded_model
    if loaded_model is None:
        print(f"Loading model from: {MODEL_OUTPUT_PATH}")
        loaded_model = joblib.load(MODEL_OUTPUT_PATH)
    return loaded_model



@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        model = get_model()

        features = np.array([[
            int(request.form["lead_time"]),
            int(request.form["no_of_special_request"]),
            float(request.form["avg_price_per_room"]),
            int(request.form["arrival_month"]),
            int(request.form["arrival_date"]),
            int(request.form["market_segment_type"]),
            int(request.form["no_of_week_nights"]),
            int(request.form["no_of_weekend_nights"]),
            int(request.form["type_of_meal_plan"]),
            int(request.form["room_type_reserved"]),
        ]])

        prediction = model.predict(features)[0]

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
