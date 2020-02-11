import face_recognition as fr
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2
import re, os, secrets
from PIL import Image
from flask import current_app

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def compare_faces(file1, file2):
    # Load the jpg files into numpy arrays
    image1 = fr.load_image_file(file1)
    image2 = fr.load_image_file(file2)
    
    # Get the face encodings for 1st face in each image file
    image1_encoding = fr.face_encodings(image1)[0]
    image2_encoding = fr.face_encodings(image2)[0]
    
    # Compare faces and return True / False
    results = fr.compare_faces([image1_encoding], image2_encoding)    
    return results[0]

def save_emotion_picture(form_picture):           
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture,'r')
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def detect_emotion(img_file):
    target = ['angry','disgust','fear','happy','sad','surprise','neutral']
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    model = load_model('model_5-49-0.62.hdf5')
    img_file = os.path.join(current_app.root_path, 'static/profile_pics', img_file)
    img = image.load_img(img_file, target_size=(48,48))
    img = image.img_to_array(img)
    face_rects = face_cascade.detectMultiScale(img)
    for (x,y,w,h) in face_rects:
        face_crop = img[y:y+h, x:x+w]
        face_crop = face_crop.reshape((-1,1,48,48))
    result = target[np.argmax(model.predict(face_crop))]
    return result


def print_request(request):
    # Print request url
    print(request.url)
    # print relative headers
    print('content-type: "%s"' % request.headers.get('content-type'))
    print('content-length: %s' % request.headers.get('content-length'))
    # print body content
    body_bytes = request.get_data()
    # replace image raw data with string '<image raw data>'
    body_sub = re.sub(b'(\r\n\r\n)(.*?)(\r\n--)',br'\1<image raw data>\3', body_bytes,flags=re.DOTALL)
    print(body_sub.decode('utf-8'))