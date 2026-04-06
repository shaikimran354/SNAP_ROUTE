import tensorflow as tf
import numpy as np
import cv2

# Don't load at import time
model = None
class_names = None

def get_model():
    global model, class_names
    if model is None:
        print("Loading model...")
        model = tf.keras.models.load_model("data/mobilenetv2_gru_model.h5")
        class_names = np.load("data/class_names.npy", allow_pickle=True).tolist()
        print("Model loaded!")
    return model, class_names

def classify_image(img_array: np.ndarray) -> str:
    m, names = get_model()
    if img_array.ndim == 2:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    img_resized = cv2.resize(img_array, (224, 224))
    processed   = np.expand_dims(img_resized / 255.0, axis=0).astype(np.float32)
    prediction  = m.predict(processed, verbose=0)
    return names[np.argmax(prediction)].strip()