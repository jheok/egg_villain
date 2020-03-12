import cv2
import os
import shutil
import glob
import time
import datetime


body_cascade = cv2.CascadeClassifier('fullbody/haarcascade_fullbody.xml')

#C:\Users\jh\Desktop\python_workspace home
#workspace_home_path

def image_find():
    dest_dir = 'D:\\01attribute_prediction'

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)


    for files in glob.glob('img_highres/**/**/**.**', recursive=True):
        img_path = files
        print(files)
        file = os.path.basename(files)
        file_path = os.path.dirname(files)

        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bodys = body_cascade.detectMultiScale(gray, 1.01, 20, minSize=(40,50))

        if len(bodys) == 0:
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