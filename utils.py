# utils.py
import numpy as np
import onnxruntime as ort
import time

def preprocess_image(image):
    image = image.resize((224, 224))
    img_array = np.array(image).astype("float32") / 255.0
    img_array = np.transpose(img_array, (2, 0, 1))  # channels first
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(model_path, img_array):
    session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
    start = time.time()
    logits = session.run(None, {session.get_inputs()[0].name: img_array})[0][0]
    end = time.time()
    exp_logits = np.exp(logits - np.max(logits))
    probs = exp_logits / exp_logits.sum()
    return probs, end - start


def render_confidence_bar(pred_class, confidence, inference_time):
    return f"""
    <div style='background: #1e2130; padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
        <h4 style='color:#00ffcc;'>🔍 Prediction: <span style='color:white'>{pred_class}</span></h4>
        <div style='background:#333; border-radius:10px; overflow:hidden; height:24px;'>
            <div style='width:{confidence:.2f}%; background:#00cc88; color:white; padding:2px 0; text-align:center; font-weight:bold;'>
                {confidence:.2f}% Confidence
            </div>
        </div>
        <small style='color: #aaa;'>Inference Time: {inference_time:.2f} seconds</small>
    </div>
    """

