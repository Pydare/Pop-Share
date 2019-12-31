import face_recognition as fr
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import re

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

def detect_emotion(img_file):
    target = ['angry','disgust','fear','happy','sad','surprise','neutral']
    model = load_model('model_5-49-0.62.hdf5')
    img = image.load_img(img_file, target_size=(48,48))
    img = image.img_to_array(img)
    img = img.reshape((-1,1,48,48))
    p = np.argmax(model.predict(img))
    if p > 6:
        p = 6
    return target[p]


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