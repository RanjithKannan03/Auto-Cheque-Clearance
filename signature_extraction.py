import cv2
import numpy as np

def extract_signature(input_path):
    # Load the image
    image_path = input_path
    image = cv2.imread(image_path)

   # Get image dimensions
    height, width, _ = image.shape

    # Define the region of interest (bottom right quarter)
    start_x = width // 2
    start_y = height // 2
    end_x = width
    end_y = height

    # Crop the bottom right quarter from the image
    roi = image[start_y:end_y, start_x:end_x]

    # Convert ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to obtain binary image
    binary = cv2.adaptiveThreshold(gray_roi, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 10)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through contours to identify signature
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Filter out small contours to avoid noise
            # Approximate the contour to a polygon
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            x, y, w, h = cv2.boundingRect(contour)
            signature = roi[y:y+h, x:x+w]
            cv2.imwrite(r"sign2.png", signature)
    print("Signature extracted and saved successfully!")




