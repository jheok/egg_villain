
########################
#                                       #
#       주석 지우지 말것
#       kivy                           #
#       커뮤니티 활동
#       yona
#       okky
#       분석 설계 구현 검증
#                                       #
########################

import time
import locale
import requests
import json
import feedparser
import threading
import datetime


from random import sample
from tkinter import *
from tkinter import ttk

from tkinter import messagebox
from PIL import Image, ImageTk
from contextlib import contextmanager

import imageio      #비디오
video_name = "bandicam 2020-02-19 17-09-45-552.mp4" #This is your video file path
video = imageio.get_reader(video_name)

text_xsmall = 15
text_small = 20
text_medium = 25
text_big = 45
text_xlarge = 90

latitude = None
longitude = None

weather_api = '0f4eba3ba474e004be5a7b11986d8bd6'
weather_lang = 'ko'
weather_unit = 'auto'

weather_icons = {
    'clear-day': 'weather_icon/Sun.png',
    'wind': 'weather_icon/Wind.png',
    'cloudy': 'weather_icon/Cloud.png',
    'partly-cloudy-day': "weather_icon/PartlySunny.png",
    'rain': "weather_icon/Rain.png",
    'snow': "weather_icon/Snow.png",
    'snow-thin': "weather_icon/Snow.png",
    'fog': "weather_icon/Haze.png",
    'clear-night': "weather_icon/Moon.png",
    'partly-cloudy-night': "weather_icon/PartlyMoon.png",
    'thunderstorm': "weather_icon/Storm.png",
    'tornado': "weather_icon/Tornado.png",
    'hail': "weather_icon/Hail.png"
}

recommend_icon = 'recommend_icon/recommend.png'
youtube_icon = 'youtube_icon/playButton.png'

class Time(Frame):

    def __init__(self, parent, *args, **krwargs):
        Frame.__init__(self, parent, bg='black')

        # Get Time
        self.time = time.strftime('%H:%M')
        self.date = time.strftime('%A, %d. %B')

        # Make Time Labels
        self.timeLabel = Label(self, font=(
            'Helvetica', text_big), text=self.time, fg='white', bg='black')
        self.dateLabel = Label(self, font=(
            'Helvetica', text_small), text=self.date, fg='white', bg='black')

        # Display Labels
        self.timeLabel.pack(side=TOP, anchor=W)
        self.dateLabel.pack(side=TOP, anchor=W)


class Weather(Frame):

    def get_ip(self):
        try:
            url = 'http://jsonip.com'
            req = requests.get(url)
            ip_json = json.loads(req.text)
            ip = ip_json['ip']
            return ip

        except Exception as e:
            return 'Error: %s. Cannot get ip'

    def get_weather(self):
        try:
            if latitude is None and longitude is None:
                # get location
                api_key = 'df8e1a9da2cf6464817b3b30e43c08ce'  # IP Stack Api Key
                url = 'http://api.ipstack.com/{}?access_key={}'.format(self.get_ip(), api_key)
                req = requests.get(url)
                res = json.loads(req.text)

                # set location
                lat = res['latitude']
                lon = res['longitude']
                location2 = '%s' % (res['city'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                    weather_api, lat, lon, weather_lang, weather_unit)
            else:
                location = ''
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                    weather_api, latitude, longitude, weather_lang, weather_unit)

            req = requests.get(weather_req_url)
            weather = json.loads(req.text)

            degree_sign = u'\N{DEGREE SIGN}'
            temperature2 = '{}{}'.format(
                int(weather['currently']['temperature']), degree_sign)
            weather_summary2 = weather['currently']['summary']
            icon_id = weather['currently']['icon']
            weather_icon2 = None

            if icon_id in weather_icons:
                weather_icon2 = weather_icons[icon_id]

            if weather_icon2 is not None:
                if self.weather_icon != weather_icon2:
                    self.weather_icon = weather_icon2
                    image = Image.open(weather_icon2)
                    image = image.resize((65, 65), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLabel.config(image=photo)
                    self.iconLabel.image = photo
            else:
                # remove image
                self.iconLabel.config(image='')

            # set attributes
            if self.weather_summary != weather_summary2:
                self.weather_summary = weather_summary2
                self.summaryLabel.config(text=weather_summary2)

            if self.temperature != temperature2:
                self.temperature = temperature2
                self.tempLabel.config(text=temperature2)

            if self.location != location2:
                if location2 == ', ':
                    self.location = '지역을 찾을수 없습니다'
                    self.locationLabel.config(text='지역을 찾을수 없습니다')
                else:
                    self.location = location2
                    self.locationLabel.config(text='지역 : {}'.format(location2))


        except Exception as e:
            print('Error {}. 날씨를 찾을수 없습니다'.format(e))

        self.after(60000, self.get_weather)

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # Init attributes
        self.temperature = ''
        self.location = ''
        self.weather_summary = ''
        self.weather_icon = None
        # Make Widgets
        self.weather_frame = Frame(self, bg='black')
        self.weather_frame.pack(side=TOP, anchor=W)

        self.tempLabel = Label(self.weather_frame, font=(
            'Helvetica', text_xlarge), fg='white', bg='black')
        self.tempLabel.pack(side=LEFT, anchor=N)

        self.iconLabel = Label(self.weather_frame, bg='black')
        self.iconLabel.pack(side=LEFT, anchor=N, padx=20, pady=20)

        self.summaryLabel = Label(self, font=(
            'Helvetica', text_small), fg='white', bg='black')
        self.summaryLabel.pack(side=TOP, anchor=E)

        self.locationLabel = Label(self, font=(
            'Helvetica', text_xsmall), fg='white', bg='black')
        self.locationLabel.pack(side=TOP, anchor=E)

        self.get_weather()


class Recommend(Frame):

    def click(self, event):
        messagebox.showinfo("message box", "recommend program")


    def __init__(self, parent, *args, **krwargs):
        Frame.__init__(self, parent, bg='black')
        # Init attributes

        # make Label
        Label(self, text="Youtube", font=('Helvetica', text_xsmall), fg='white',
              bg='black').pack(side=BOTTOM, pady=10)

        #setting image
        image = Image.open(recommend_icon)
        image = image.resize((200, 240), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        # make button
        label = Label(self, image=photo, bg='black')
        label.image = photo
        label.bind("<Button>", self.click)
        label.pack(side=BOTTOM, anchor=W)

class Tube(Frame):



    def __init__(self, parent, *args, **krwargs):
        Frame.__init__(self, parent, bg='black')

        # Init attributes

        # make Label
        Label(self, text="Youtube", font=('Helvetica', text_xsmall), fg='white',
              bg='black',).pack(side=BOTTOM, pady=10)

        #setting image
        image = Image.open(youtube_icon)
        image = image.resize((240, 200), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        # make button
        label = Label(self, image=photo, bg='black')
        label.image = photo
        label.bind("<Button>", self.click)
        label.pack(side=BOTTOM, anchor=W)

    #비디오 플레이        #미완성
    def stream(self):
        for image in video.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image))
            self.config(image=frame_image)
            self.image = frame_image

    def click(self, event):
        #messagebox.showinfo("massage Box", "Youtube")
        thread = threading.Thread(target=self.stream, args=(self,))
        thread.daemon = 1
        thread.start()

class Screen:

    def __init__(self):
        self.tk = Tk()
        self.state = False
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background='black')
        self.bottomFrame = Frame(self.tk, background='black')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.centerTopFrame = Frame(self.tk, background='black')
        self.centerTopFrame.pack(side=TOP, fill=X, expand=YES)
        self.centerBottomFrame = Frame(self.tk, background='black')
        self.centerBottomFrame.pack(side=TOP, fill=Y, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.tk.bind('<Return>', self.toggle_fullscreen)
        self.tk.bind('<Escape>', self.end_fullscreen)

        self.time = Time(self.topFrame)
        self.time.pack(side=LEFT, anchor=N, padx=100, pady=60)

        self.weather = Weather(self.topFrame)
        self.weather.pack(side=RIGHT, anchor=N, padx=100, pady=60)

        self.recommend = Recommend(self.bottomFrame)
        self.recommend.pack(side=LEFT, anchor=N, padx=50, pady=20)

        self.tube = Tube(self.bottomFrame)
        self.tube.pack(side=RIGHT, anchor=N, padx=50, pady=20)


    # def quit(self):
    #     self.tk.destroy()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)
        return 'break'

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes('-fullscreen', False)
        return 'break'


if __name__ == '__main__':
    w = Screen()
    w.tk.mainloop()