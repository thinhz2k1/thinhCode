from __future__ import print_function
import cv2
import requests
import json

addr = 'http://192.168.38.154:5000'
# api_url = addr + '/api/loadimage'
api_url = addr + '/api/loadimage'

content_type = 'image/jpeg'
headers = {'content-type': content_type}

def ImageToServer(img,id):
    header={'id': id}
    _,img_encoded = cv2.imencode('.jpg', img)
    response = requests.post(api_url, data=img_encoded.tobytes() , headers=header)
    # print(json.loads(response.text))
    print(response.text)

img=cv2.imread('test/anh_test.jpg')
ImageToServer(img,'1')