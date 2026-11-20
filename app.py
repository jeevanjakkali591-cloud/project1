from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained ML model
model = joblib.load("multiplier_model.pkl")


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# DASHBOARD PAGE
# =========================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# =========================
# PREDICTION
# =========================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        A = float(data["A"])
        B = float(data["B"])

        dataset = pd.read_csv("dataset.csv")

        matching_rows = dataset[
            (dataset["A"] == A) &
            (dataset["B"] == B)
        ]

        # =========================
        # INPUT EXISTS IN DATASET
        # =========================

        if not matching_rows.empty:

            design1 = matching_rows[
                matching_rows["design"] == "Design 1"
            ]

            if not design1.empty:

                row = design1.iloc[0]

                Y = float(row["Y"])
                area = float(row["area"])
                accuracy = float(row["accuracy"])
                prediction_error = float(row["error"])

            else:

                prediction = model.predict(
                    pd.DataFrame(
                        [[A, B]],
                        columns=["A", "B"]
                    )
                )

                Y = A * B
                area = float(prediction[0][1])
                accuracy = float(prediction[0][2])
                prediction_error = float(prediction[0][3])

        # =========================
        # NEW INPUT
        # =========================

        else:

            Y = A * B

            prediction = model.predict(
                pd.DataFrame(
                    [[A, B]],
                    columns=["A", "B"]
                )
            )

            area = float(prediction[0][1])
            accuracy = float(prediction[0][2])
            prediction_error = float(prediction[0][3])


        # =========================
        # SEND RESULT TO WEBPAGE
        # =========================

        result = {

            "A": round(A, 2),

            "B": round(B, 2),

            "Y": round(Y, 2),

            "area": round(area, 2),

            "accuracy": round(accuracy, 2),

            "prediction_error": round(
                prediction_error, 2
            ),

            "design": "Design 1"

        }

        return jsonify(result)


    except Exception as e:

        return jsonify({

            "system_error": str(e)

        }), 500


# =========================
# RESULT PAGE
# =========================

@app.route("/result")
def result():

    return render_template(
        "result.html"
    )


# =========================
# GRAPH ANALYSIS PAGE
# =========================

@app.route("/graphs")
def graphs():

    return render_template(
        "graphs.html"
    )


# =========================
# CIRCUIT ANALYSIS PAGE
# =========================

@app.route("/circuit")
def circuit():

    return render_template(
        "circuit.html"
    )


# =========================
# REAL CIRCUIT DESIGN PAGE
# =========================

@app.route("/real-circuit")
def real_circuit():

    return render_template(
        "real_circuit.html"
    )


# =========================
# GRAPH DATA
# =========================

@app.route("/graph-data")
def graph_data():

    data = pd.read_csv(
        "dataset.csv"
    )

    return jsonify(
        data.to_dict(
            orient="records"
        )
    )


# =========================
# START FLASK
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )