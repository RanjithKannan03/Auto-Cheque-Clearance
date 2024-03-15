# Auto-Cheque-Clearance
Faster Cheque Clearing

This is an application that provides a complete all one on solution to the banking problems involved when handling large volumes of cheques in the clearning process.
The process involves many technical verifications including signature verification. Some of these steps are manual and require human intervention to complete the process. 
The current process requires the high human capital deployment and longer processing time.

# Our Solution:
We have developed a complete python based application to solve this issue. The application upon appropriate login allows users to enter their cheques. The cheque is then scanned for all the necessary details and will be validated. The signature of the payee is also validated to assur there is not fraud invloved.

# Basic workflow:

Cheque Input: 
Users enter the cheque details into the application. This can be done by uploading an image of the cheque.

Cheque Scanning: 
The application scans the cheque image to extract necessary details such as the cheque number, amount, date, and payee's signature.

Signature Validation: 
The payee's signature is extracted from the cheque image and compared against a reference signature to validate its authenticity. This can be done using a similarity score

Fraud Detection: If the signature does not match or there are other discrepancies, the application can flag the cheque as potentially fraudulent.

Validation Result: The application displays the validation result to the user, indicating whether the cheque is valid or not.

Logging and Reporting: Details of the cheque validation process, including the validation result, can be logged and reported for record-keeping and audit purposes.

Screenshots:
Custom model:
![WhatsApp Image 2024-03-15 at 14 37 23_567b9aea](https://github.com/RanjithKannan03/Auto-Cheque-Clearance/assets/34032949/d91b196c-47f3-426d-ad8f-fb65abc1aa9a)
Dataset:
![WhatsApp Image 2024-03-15 at 14 37 23_22f1b06b](https://github.com/RanjithKannan03/Auto-Cheque-Clearance/assets/34032949/d51f9ee4-0db1-463a-b6cf-75bc73d81258)
Fields:
![WhatsApp Image 2024-03-15 at 14 37 24_b15e2510](https://github.com/RanjithKannan03/Auto-Cheque-Clearance/assets/34032949/5600b7a5-5bfd-4f6d-a626-e4917af0d81b)


# Tech stack:
Firebase Setup: Set up a Firebase project and configure the necessary services (Firestore or Realtime Database).
Database Structure: Define the structure of your database to store bank details.
Integration: Integrate Firebase SDK into your application to interact with the database.
Store Bank Details: Use Firebase SDK to store bank details securely.

Segmentation in image processing involves partitioning an image into multiple segments or sets of pixels to simplify its representation or make it more meaningful for analysis. The process starts with acquiring the image, followed by preprocessing to enhance features or reduce noise. Next, relevant features are extracted from the image, such as color, texture, or intensity gradients. These features are then used in segmentation algorithms, which divide the image into meaningful regions or objects using techniques like thresholding, clustering, edge detection, region growing, or watershed segmentation. After segmentation, post-processing may be applied to refine the segmented regions, such as merging adjacent regions or smoothing boundaries. Finally, the segmented regions are analyzed and interpreted to extract meaningful information or features from the image, such as account number, bank details and signature

Signature is the most important component of the model where only if the signature matches the cheque will be labeled genuine. This is done using OpenCV and tensorflow, where a cnn (like the Siamese model) is trained on a set of genuine and forged data and is fine tuned later. The final model is saved and prediction is done based on the signature in the cheque and the signature in the database (in this case the details in the firebase database)

In conclusion, our Python-based application provides a robust solution for cheque validation, ensuring the security and authenticity of financial transactions. By leveraging image processing techniques and machine learning models, we enable users to scan cheques for necessary details and validate the payee's signature, mitigating the risk of fraud. Overall, our application streamlines the cheque validation process, offering a reliable and efficient tool for financial transactions.
