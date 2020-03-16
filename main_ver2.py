# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets# pip install pyqt5(pip install python3-pyqt5)
# from PyQt5.QtWidgets import QPushButton, QLineEdit, QInputDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
# import forecastio  # pip install python-forecastio  [Weather api] [https://github.com/ZeevG/python-forecast.io]
import yapi  # pip install yapi [https://github.com/ahmetkotan/yapi]
import datetime
from time import sleep
import threading
import tkinter as tk  # this can't pip install
import requests
import json
import cv2
import pafy  # pip install pafy , pip install youtube_dl
from PIL import Image, ImageTk
from tkinter import *



# ==================================================================================================
# ==============UI_MAIN==============================================================================
# ==================================================================================================

# class Ui_MainWindow(object):
class Ui_MainWindow(QWidget):
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    play_or_pause = True
    start = True

    def __init__(self):
        super().__init__()
        self.setupUi(MainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

        MainWindow.setPalette(palette)
        MainWindow.resize(1280, 720)
        # MainWindow.showFullScreen()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 옷 추천 버튼 =================================================================
        # self.recommendation_button = QtWidgets.QPushButton("Recommendation", self.centralwidget)
        self.recommendation_button = QtWidgets.QPushButton("", self.centralwidget)
        self.recommendation_button.setGeometry(50, 500, 300, 300)
        self.recommendation_button.setStyleSheet("image:url(Icon/Recommendation.png); border:0px")
        self.recommendation_button.clicked.connect(self.Recommendation_clicked)

        self.recommendation_label = QtWidgets.QLabel(self.centralwidget)
        self.recommendation_label.setGeometry(QtCore.QRect(100, 825, 300, 30)) # + 50
        self.recommendation_label.setObjectName("recommendation_label")
        self.recommendation_label.setFont(QtGui.QFont("맑은 고딕", 15))
        self.recommendation_label.setStyleSheet("Color: white")
        self.recommendation_label.setText("오늘의 옷 추천")

        # Youtube 버튼 ======================================================================
        # self.youtube_button = QtWidgets.QPushButton("Youtube", self.centralwidget)
        self.youtube_button = QtWidgets.QPushButton("", self.centralwidget)
        self.youtube_button.setGeometry(500, 500, 300, 300)
        self.youtube_button.setStyleSheet("image:url(Icon/YouTube.png); border:0px")
        self.youtube_button.clicked.connect(self.video_thread)

        self.youtube_label = QtWidgets.QLabel(self.centralwidget)
        self.youtube_label.setGeometry(QtCore.QRect(590, 825, 300, 30)) # + 90
        self.youtube_label.setObjectName("youtube_label")
        self.youtube_label.setFont(QtGui.QFont("맑은 고딕", 15))
        self.youtube_label.setStyleSheet("Color: white")
        self.youtube_label.setText("YouTube")

        # 날씨 이모티콘 ====================================================================
        self.weather = QtWidgets.QLabel(self.centralwidget)
        self.weather.setGeometry(QtCore.QRect(20, 15, 150, 130))
        self.weather.setObjectName("weather")

        # 온도 label [온도 출력]
        self.temperature = QtWidgets.QLabel(self.centralwidget)
        self.temperature.setGeometry(QtCore.QRect(25, 120, 150, 130))
        self.temperature.setObjectName("temperature")
        self.temperature.setFont(QtGui.QFont("맑은 고딕", 20))

        # ================================================================================
        # time 이라는 이름으로 label 생성 [(오전/오후)시/분]
        self.time = QtWidgets.QLabel(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(170, 80, 800, 60))
        self.time.setObjectName("time")
        # setFont(QtGui.QFont("Font_name",Font_size))
        self.time.setFont(QtGui.QFont("맑은 고딕", 50))

        # date 이라는 이름으로 label 생성 [년/월/일]
        self.date = QtWidgets.QLabel(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(180, 15, 300, 50))
        self.date.setObjectName("date")
        self.date.setFont(QtGui.QFont("맑은 고딕", 20))
        # ===============================================================================
        # clock_button 이라는 이름으로 버튼을 생성 [쓰레드가 잘 작동하는지 확인]
        # self.clock_button = QtWidgets.QPushButton(self.centralwidget)
        # self.clock_button.setGeometry(QtCore.QRect(200, 280, 75, 23))
        # self.clock_button.setObjectName("clock_button")

        # self.youtube_button = QtWidgets.QPushButton(self.centralwidget)
        # self.youtube_button.setGeometry(QtCore.QRect(1500, 450, 75, 23))
        # self.youtube_button.setObjectName("youtube_button")
        # ===================================================================
        #====================================================================
        #video_viewer_label 생성 =====================================================
        self.video_viewer_label = QtWidgets.QLabel(self.centralwidget)
        self.video_viewer_label.setGeometry(QtCore.QRect(900, 300, 800, 450))
        self.video_viewer_label.setObjectName("video_viewer_label")

        self.video_name_label = QtWidgets.QLabel(self.centralwidget)
        self.video_name_label.setGeometry(QtCore.QRect(900, 775, 800, 25))
        self.video_name_label.setObjectName("video_name_label")
        self.video_name_label.setFont(QtGui.QFont("맑은 고딕", 11))

        #===================================================================
        #===================================================================

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SmartMirror"))
        # self.clock_button.setText(_translate("MainWindow", "PushButton"))
        # self.youtube_button.setText(_translate("MainWindow", "Youtube"))

    # -----------------------------------------------------------------------------------------
    # 이벤트
    # EVENT
    # -----------------------------------------------------------------------------------------

    # 시간을 알려주는 함수 메인 화면에 생성
    # now.(year,month,day,hour,minute,second)
    def set_time(self, MainWindow):
        EvenOrAfter = "오전"
        while True:
            now = datetime.datetime.now()  # 현재 시각을 시스템에서 가져옴
            hour = now.hour

            if (now.hour >= 12):
                EvenOrAfter = "오후"
                hour = now.hour % 12

                if (now.hour == 12):
                    hour = 12

            else:
                EvenOrAfter = "오전"

            self.date.setText("%s년 %s월 %s일" % (now.year, now.month, now.day))
            self.time.setText(EvenOrAfter + " %s시 %s분" % (hour, now.minute))
            sleep(1)

    # 옷 추천 프로그램 ========================================================
    def Recommendation_clicked(self, MainWindow):
        dlg = Recommend_dialog()
        dlg.exec_()
        # 이 밑으로 실행 안됨
        style = str(dlg.style)
        print(style)


    def Get_videoId(self, MainWhindow):
        # while True:
            url = "https://youtu.be/"

            api = yapi.YoutubeAPI('AIzaSyDerAoBBy_e9nSHggcX7C8cePReMnfzlvU')
            video_name = "홈트레이닝" #"자막뉴스 "
            results = api.general_search(video_name, max_results=2)

            str_results = str(results)

            i = 0
            TrueOrFalse = False
            video_id = ""

            # print(str_results)

            while True:
                try:

                    if "'" in str_results[i]:
                        if "=" in str_results[i - 1]:
                            if "d" in str_results[i - 2]:
                                if "I" in str_results[i - 3]:
                                    if "o" in str_results[i - 4]:
                                        i = i + 1
                                        TrueOrFalse = True
                                        break
                    i = i + 1

                except IndexError as e:
                    print("error")
                    break

            while TrueOrFalse:
                if "'" in str_results[i]:
                    break
                else:
                    video_id = video_id + str_results[i]

                i = i + 1

            url = url + video_id

            try:
                vPafy = pafy.new(url)
                self.video_name_label.setText(vPafy.title)
                video_length = vPafy.length / 60

            except Exception as e:
                self.video_viewer_label.setText("Error")
                self.start = False
            # print(video_length / 60)

            play = vPafy.getbest(preftype="mp4")
            cap = cv2.VideoCapture(play.url)
            self.ret, self.frame = cap.read()

            return cap


    def Video_to_frame(self, MainWindow):
        cap = self.Get_videoId(MainWindow)
        self.ret, self.frame = cap.read()

        while self.play_or_pause:
            self.ret, self.frame = cap.read()
            if self.ret:
                self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                                QImage.Format_RGB888)

                self.pixmap = QPixmap(self.convertToQtFormat)
                self.p = self.pixmap.scaled(800, 450, QtCore.Qt.IgnoreAspectRatio)

                self.video_viewer_label.setPixmap(self.p)
                self.video_viewer_label.update()

                sleep(0.02)  # Youtube 영상 1프레임당
                self.Pause_video(MainWindow)
            else:
                break

        cap.release()
        cv2.destroyAllWindows()


    def Clicked_pause(self, MainWindow):
        if self.play_or_pause == True:
            self.play_or_pause = False
        else:
            self.play_or_pause = True


    def Pause_video(self, MainWindow):
        while True:
            if self.play_or_pause == True:
                break


    def Stop_video(self, MainWindow):
        if self.video_thread.isRunning():
            self.video_thread.terminate() # 현재 돌아가는 스레드 중지
        else:
            self.video_thread
        '''
        if self.start == True:
            self.start = False
            threading.terminate()
            print("Stop")

        else:
            self.start = True
            self.video_thread(MainWindow)
            print("Start")
        '''


    # ----------------------------------------------------------------------------------------------------
    # ------------------------ 쓰레드 ---------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------

    # Set_time을 쓰레드로 사용
    def time_start(self, MainWindow):
        thread = threading.Thread(target = self.set_time, args = (self,))
        thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()

    def Recommend_thread(self, MainWindow):
        thread = threading.Thread(target=self.Recommendation_clicked, args = (self,))
        thread.daemon = True
        threading.start()

    # video_to_frame을 쓰레드로 사용
    def video_thread(self, MainWindow):
        thread = threading.Thread(target = self.Video_to_frame, args = (self,))
        thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()

        # 재생/정지 버튼 =================================================================
        self.btn = QtWidgets.QPushButton("Play/Pause", self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(900, 825, 150, 30))
        self.btn.setObjectName("Play/Pause")
        self.btn.clicked.connect(self.Clicked_pause)
        self.btn.show()
        # ================================================================================


class Recommend_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.style = None

    def setupUI(self):
        self.setGeometry(500, 300, 300, 210)
        self.setWindowTitle("스타일 선택")

        groupBox = QGroupBox("오늘의 스타일", self)
        groupBox.move(10, 10)
        groupBox.resize(280, 180)

        self.radio1 = QRadioButton("캐주얼", self)
        self.radio1.move(20, 30)
        # self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.RadioButtonClicked)

        self.radio2 = QRadioButton("모던", self)
        self.radio2.move(20, 60)
        self.radio2.clicked.connect(self.RadioButtonClicked)

        self.radio3 = QRadioButton("로맨틱", self)
        self.radio3.move(20, 90)
        self.radio3.clicked.connect(self.RadioButtonClicked)

        self.radio4 = QRadioButton("스포츠", self)
        self.radio4.move(20, 120)
        self.radio4.clicked.connect(self.RadioButtonClicked)

        self.radio5 = QRadioButton("유니크", self)
        self.radio5.move(20, 150)
        self.radio5.clicked.connect(self.RadioButtonClicked)


    def RadioButtonClicked(self):
        style = ""
        if self.radio1.isClicked():
            style = "Casual"
        elif self.radio2.isClicked():
            style = "Modern"
        elif self.radio3.isClicked():
            style = "Romantic"
        elif self.radio3.isClicked():
            style = "Sport"
        else:
            style = "Unique"

        # self.accept()
        self.close()

    # def showModal(self):
        # return super().exec_()

# -------------메인---------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)

    ui.time_start(MainWindow)  # time thread

    # ui.video_thread(MainWindow)  # video thread

    MainWindow.show()

    sys.exit(app.exec_())