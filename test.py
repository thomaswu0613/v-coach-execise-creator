import PySimpleGUI as sg
import cv2
from time import sleep
import numpy as np
from tomlkit import value
from tools import detect_pose_with_draw, BodyLandMarks
import mediapipe as mp
layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20',)],
            [sg.Image(filename='', key='image'),sg.Listbox('',size=(30,30),key='listbox1')],
            [sg.Image(filename='', key='image1')],
            [sg.Text('', size=(40, 1), justification='center', font='Helvetica 20',key="txt1"),],
            [sg.FileBrowse('Open Video File',file_types=(("Video Files", "*.mp4",),("Video Files","*.avi"),("Video Files","*.MOV"),)),sg.Button('Load Video', size=(10, 1), font='Helvetica 14'),
            sg.Button('Create Stage', size=(10, 1), font='Any 14',key='create_stage'),
            sg.Button('Play Again', size=(10, 1), font='Any 14'),
            sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]


window = sg.Window('Demo Application - OpenCV Integration',
                    layout, location=(800, 400),return_keyboard_events=True)


video = False
pause = False
# reload = False

listboxone = []
stages_to_write = {}
mp_pose = mp.solutions.pose
frame_count = 0
stage_count = 0

while True:
    event, values = window.read(timeout=10)
    # print(event)
    if event == 'Exit' or event == sg.WIN_CLOSED or event == "Escape:9":
        for k,v in stages_to_write.items():
            print(k,v)
        window.close()
        cap.release()
        break
    if event == 'Load Video':
        video_path = values["Open Video File"]
        video = True
        pause = True
        cap = cv2.VideoCapture(video_path)
        # cap = cv2.VideoCapture("/home/thomasw/workspace/execise-creator-app/IMG_105610890.MOV")
        loading_screen_layout = [[sg.Text('Loading..', size=(40, 1), justification='center', font='Helvetica 30')],
                        [sg.ProgressBar(
                            max_value=30,
                            orientation='h',
                            size=(20, 20),
                            border_width=4,
                            key='progbar',
                            bar_color=['Red','Green'])]]

    if event == 'Play Again':
        cap = cv2.VideoCapture(video_path)
        pause = True
        video = True

    if event == 'space:65':
        pause = bool(abs(1-int(pause)))
        sleep(1)

    if event == 'create_stage':
        lm = BodyLandMarks(results, mp_pose)
        stages_to_write[stage_count] = [lm.return_all_points(),frame_count]
        print("Created stage {}".format(int(stage_count)))
        listboxone.append("Stage {}: Frame No. {}".format(str(stage_count),str(frame_count)))
        window['listbox1'].update(listboxone)
        stage_count+=1
        print(stages_to_write)
        

    if video:
        window["txt1"].update(value="Press space bar to play the video.")
        if pause:
            continue
        success, frame = cap.read()
        if not success:
            video = False
            # reload = False
            continue
        scale_percent = 60       # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        window["image"].update(data=cv2.imencode('.png', resized)[1].tobytes())
        frame, results = detect_pose_with_draw(resized)
        window["image1"].update(data=cv2.imencode('.png', frame)[1].tobytes())
        frame_count+=1
    else:
        window["txt1"].update(value="")


