from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__, static_folder='static', template_folder='src')
model = load_model("mnist_model.h5")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    img_data = data["image"].split(",")[1]
    img = Image.open(io.BytesIO(base64.b64decode(img_data))).convert("L")
    img = img.resize((28, 28))
    img_array = np.array(img).astype("float32") / 255
    img_array = img_array.reshape(1, 28, 28, 1)
    prediction = model.predict(img_array)
    return jsonify({"prediction": int(np.argmax(prediction))})

if __name__ == "__main__":
    app.run(debug=True)
