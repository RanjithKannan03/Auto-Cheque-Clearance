from tensorflow.keras.models import save_model, load_model
import numpy as np
import cv2

def validate_signature():
    def preprocess_signature(signature_path):
        signature = cv2.imread(signature_path)
        # Resize the image to 224x224 pixels
        signature = cv2.resize(signature, (224, 224))
        # Convert pixel values to range [0, 1]
        signature = signature / 255.0
        return signature

    model = load_model("new_model.h5")
    signature1_preprocessed = preprocess_signature('sign1.png') #change to original signature
    signature2_preprocessed = preprocess_signature('sign2.png') #change to signature extracted from cheque
    predictions = model.predict(np.array([signature1_preprocessed, signature2_preprocessed]))

    # Calculate Euclidean distance between the prediction vectors
    euclidean_distance = np.linalg.norm(predictions[0] - predictions[1])

    # Calculate cosine similarity between the prediction vectors
    dot_product = np.dot(predictions[0], predictions[1])
    norms = np.linalg.norm(predictions, axis=1)
    cosine_similarity = dot_product / (norms[0] * norms[1])
    print(cosine_similarity)

    def validate(cosine_similarity):
        if cosine_similarity>0.949:
            return "Matched"
        else:
            return "Unmatched"

    validate(cosine_similarity)
validate_signature()