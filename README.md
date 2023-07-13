# Posture Recognition
The system consists of a tool that uses as input an image of a person sitting in a lateral position captured by any camera, in this case an OV5647 camera, and has as output a image of the detected keypoints, determined from the OpenPose 18 keypoints architecture, and the classification of the posture in correct, incorrect or indeterminate. In case the posture is determined as incorrect, the system uses different colors to show, in the output image, which body parts led the algorithm to make this classification.

## System architecture
In general, the system architecture is as follows:

- Data collection
  - Data is collected by a camera connected to a microcontroller
- Feature extraction
  - Image preprocessing
  - Detection of keypoints
  - Calculation of angles and extraction of other information
- Classification
  - XGBoost model
  - Bayesian optimization
  - SHAP values
- User interface 
  - Presentation of classification results

## OpenPose keypoint detection architecture
- The h5 file containing the architecture weights should be stored in "PostureServer/posture_classification/" and can be obtained from the following link
- [Weights](https://www.dropbox.com/s/llpxd14is7gyj0z/model.h5)

## Screenshots of the system running (Portuguese interface)
![correct](https://github.com/imonteiroyh/PostureRecognition/assets/61994795/89f8f9f3-1481-4a57-a36d-44b6932034ff)
![incorrect-trunk](https://github.com/imonteiroyh/PostureRecognition/assets/61994795/dea45462-2be4-4e78-af27-6cb906e0f9eb)
![incorrect-up](https://github.com/imonteiroyh/PostureRecognition/assets/61994795/8c57ba71-f60f-4a54-8035-8a1a862aaee1)
![indeterminate](https://github.com/imonteiroyh/PostureRecognition/assets/61994795/8d365892-789e-4284-b386-68480cdac7e2)

## Contributions
The project was made by Vandemberg Monteiro, responsible for the feature extraction and classification, Davi Queiroz, responsible for the communication between the camera and the server and between the server and the client, and Yago Oliveira, responsible for the user interface. Data collection was structured by Vandemberg Monteiro and carried out by Davi Queiroz and Yago Oliveira.
