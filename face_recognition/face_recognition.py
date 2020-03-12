class FaceRecognition():
    import os
    import sys
    import requests

    client_id = "kJE6_Me4KcxkDvJ_JIKI"
    client_secret = "QC1yX6yao0"

    url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
    files = {'image': open('유재석.png', 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url, files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
        print (response.text)
    else:
        print("Error Code:" + rescode)

    import json

    print(json.dumps(json.loads(response.text), indent = 4, ensure_ascii=False))

    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import matplotlib.patches as patches
    import numpy as np
    import json
    detect_result = json.loads(response.text)
    import cv2
    detect_result

    detect_summary = detect_result['faces'][0]
    x, y, w, h = detect_summary['roi'].values()
    gender, gen_confidence = detect_summary['gender'].values()
    emotion, emotion_confidence = detect_summary['emotion'].values()
    age, age_confidence = detect_summary['age'].values()

    import random
    rand = random.randint(1, 100)
    file_name = f'{rand}.png'


    #======================================================================

    from matplotlib.pyplot import imshow
    import numpy as np
    from PIL import Image

    img_face = Image.open('유재석.png')
    img_face_cropped = img_face.crop((x-30, y-30, x+w+50, y+h+50))
    img_face_cropped.show()
    img_face_cropped.save(file_name)
    img_logo_bmp = Image.open("유재석_cropped.png")

    #======================================================================
    result = []
    annotation = gender + ' : ' + str(gen_confidence) + \
                    '\n' + emotion + ' : ' + str(emotion_confidence) + \
                    '\n' + age + ' : ' + str(age_confidence)+'\n'
    print(annotation)


    result.append(gender)
    result.append(emotion)
    result.append(age)

    print(result)

    f = open(f'{file_name}.txt', mode = 'wt', encoding = 'utf-8')
    f.write(gender+'\n')
    f.write(emotion+'\n')
    f.write(age+'\n')
    f.close()