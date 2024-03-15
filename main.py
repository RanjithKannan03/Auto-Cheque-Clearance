import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import pandas as pd
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import streamlit as st
import urllib.request
from PIL import Image
from signature_extraction import extract_signature


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'turnkey-banner-417205-e419c97253ef.json'

cred = credentials.Certificate('hackathon-5b333-firebase-adminsdk-y1wdm-10a7da0491.json')
# app = firebase_admin.initialize_app(cred)


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


def online_process(
        project_id: str,
        location: str,
        processor_id: str,
        file_path: str,
        mime_type: str,
) -> documentai.Document:
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()
        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type
        )
        request = documentai.ProcessRequest(
            name=resource_name, raw_document=raw_document
        )
        result = documentai_client.process_document(request=request)
        return result.document


def backend():
    project_id = 'turnkey-banner-417205'
    location = 'eu'
    processor_id = '58fa9a7f5c31ac32'
    processor_version = 'rc'
    file_path = "uploadedCheques/cheque.png"  # uploaded cheque image
    mime_type = 'image/png'
    document = online_process(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        file_path=file_path,
        mime_type=mime_type,
    )
    l = []
    for i in document.entities:
        lst = []
        lst.append(i.type_)
        lst.append(i.text_anchor.content)
        lst.append(i.confidence)
        l.append(lst)
    print(l)

    for i in l:
        i[1] = i[1].replace(" ", "")
    print(l)

    acNo = 0
    ifs = 0
    for i in l:
        if i[0] == 'AcNo':
            acNo = int(i[1])
    for i in l:
        if i[0] == 'IFS':
            ifs = i[1]
    print(acNo)
    print(ifs)



    db = firestore.client()

    ref = db.collection("centralized")
    docs = ref.where('AcNo', '==', acNo).where('IFSC', '==', ifs).stream()

    d = {}
    for doc in docs:
        d = doc.to_dict()
        print(doc.id)
        print(doc.to_dict())

    acno1 = int(st.number_input("Enter your Account number:"))
    phno1 = int(st.number_input("Enter your Mobile number:"))
    docs1 = ref.where('AcNo', '==', acno1).where('PhNo', '==', phno1).stream()

    d1 = {}
    for doc1 in docs1:
        d1 = doc1.to_dict()
        print(doc1.id)
        print(doc1.to_dict())

    st.subheader("Payee Details:")
    for (key, value) in d1.items():
        if key != 'Sign':
            st.write(f"{key}: {value}")

    st.subheader("Payer Details:")
    for (key, value) in d.items():
        if key != 'Sign':
            st.write(f"{key}: {value}")

    st.subheader("Cheque Details:")

    criteria=['AcNo','IFS','Pay']

    fields=[_[0] for _ in l]
    print(fields)
    if 'Rupees' not in fields and 'RupeesNumber' not in fields:
        st.write("Check Returned, please upload a better photo.")
        return None

    for li in l:
        if li[0] in criteria:
            if float(li[2]<0.7):
                st.write("Check Returned, please upload a better photo.")
                return None
            else:
                st.write(f"{li[0]} : {li[1]}")
        if 'Rupees' == li[0]:
            s=list(li[1])
            for i in range(0,len(s)-1):
                if s[i+1].isupper():
                    s[i]=s[i]+' '
            li[1]="".join(s)
            st.write(f"{li[0]} : {li[1]}")
        elif 'RupeesNumber' == li[0]:
            st.write(f"{li[0]} : {li[1]}")

    extract_signature(file_path)
    path1 = d['Sign']
    path2 = 'sign2.png'  # Path to identified sign
    urllib.request.urlretrieve(path1, "sign1.png")
    similarity_value = match("sign1.png", path2)

    print("Similarity:", similarity_value)
    if similarity_value > 80:
        st.write("Cheque passed")
    else:
        st.write("Cheque Bounced")
    # print(validate_signature())





# Compare Signature
def removeWhiteSpace(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255 * (gray < 128).astype(np.uint8)
    coords = cv2.findNonZero(gray)
    x, y, w, h = cv2.boundingRect(coords)
    rect = img[y:y + h, x:x + w]
    return rect


def match(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    img1 = removeWhiteSpace(img1)
    img2 = removeWhiteSpace(img2)

    # Convert images to grayscale
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Resize images for comparison
    gray_img1 = cv2.resize(gray_img1, (300, 300))
    gray_img2 = cv2.resize(gray_img2, (300, 300))

    # Detect contours
    contours_img1, _ = cv2.findContours(gray_img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_img2, _ = cv2.findContours(gray_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on images
    cv2.drawContours(img1, contours_img1, -1, (0, 255, 0), 2)
    cv2.drawContours(img2, contours_img2, -1, (0, 255, 0), 2)

    # Display images with contours
    # cv2.imshow("Contours One", img1)
    # cv2.imshow("Contours Two", img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Calculate structural similarity index
    similarity_value = ssim(gray_img1, gray_img2, gaussian_weights=True, sigma=1.2, use_sample_covariance=False)
    similarity_percent = similarity_value * 100
    print("Similarity value: {:.2f}%".format(similarity_percent))
    return similarity_percent


def saveImage(fileUpload, folderPath):
    file = fileUpload.read()
    fileName = "cheque.png"

    # Create the folder if it does not exist
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    # Save the image to the folder
    with open(os.path.join(folderPath, fileName), "wb") as f:
        f.write(file)



division_box_html = """
<div style="background-color: rgba(255,255,255,0.4); padding: 20px; border-radius: 10px; text-align: center;">
    <h1 style="color: #000000; font-size: 36px;">Welcome to the Automatic Cheque Clearance</h1>
    <img width="96" height="96" src="https://img.icons8.com/glyph-neue/64/bank.png" alt="trust--v1"/>
    <p style="color: #000000; font-size: 18px;">Upload a picture of the cheque and enter your account number</p>
</div>
"""
# Render the weather-themed design
st.markdown(division_box_html, unsafe_allow_html=True)
st.text(" ")
st.text(" ")
uploaded_file = st.file_uploader("Upload your image here...", type=["png","jpg"])
if uploaded_file is not None:
    saveImage(uploaded_file, "UploadedCheques")
    # # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    backend()




st.markdown("<hr>", unsafe_allow_html=True)


