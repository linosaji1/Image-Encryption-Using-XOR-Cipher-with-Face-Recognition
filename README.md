# Introduction
* The code utilizes Tkinter and customtkinter for the GUI.
* It authenticates users' faces and searches their details in a MySQL database.
* Upon successful authentication, it enables users to encrypt or decrypt images.
* Encryption and decryption functions XOR the image bytes with the generated key to perform the operation.
* A unique key is generated for each user.

# Requirements

```
pip install Pillow
```
```
pip install mysql-connector-python
```
```
pip install opencv-python
```
```
pip install mtcnn
```
```
pip install tensorflow==2.15.0
```
```
pip install scikit-learn
```
```
pip install customtkinter
```

# How to Run
* Open a terminal or command prompt.
* Navigate to the directory where your Python script is located.
* Run the script by executing the following command:
	* python main.py
* Upon running the script, a GUI window will appear for authentication.
* You can choose to encrypt or decrypt an image.
* The encryption/decryption process will be performed on the selected image file.

  ** Make sure to replace the database credentials (host, user, password) in the database.py code with your actual MySQL database credentials.

* Create a folder named "Faces" inside the Face_detect folder

* If the face data is deleted from Face_detect/Faces, run the t.py code before running main.py.
