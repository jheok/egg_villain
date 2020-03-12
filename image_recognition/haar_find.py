import cv2
import os
import shutil
import glob
import time
import datetime


face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontface.xml')

#C:\Users\jh\Desktop\python_workspace home
#workspace_home_path

def image_find():
    dest_dir = 'D:\\landmark'

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # attribute_prediction은 중간에 .찍혀 있는 폴더명이 존재함
    # 중간에 폴더지워가면서 해줘야함
    for files in glob.glob('landmark/**/**.**', recursive=True):
        img_path = files
        print(files)
        file = os.path.basename(files)
        file_path = os.path.dirname(files)

        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)

        if len(faces) == 0:
            if not os.path.exists(dest_dir + '\\' + file_path):
                os.makedirs(dest_dir + '\\' + file_path)
            shutil.move(files, dest_dir + '\\' + file_path + '\\' + file)
        else:
            continue


if __name__ =='__main__':
    start = time.time()
    image_find()
    sec = time.time()-start
    times = str(datetime.timedelta(seconds=sec)).split(".")
    times = times[0]
    print(times)

#얼굴 없는 이미지를 출력한다