from email import message
import traceback
from turtle import title
import PySimpleGUI as sg
import cv2
from time import sleep
import numpy as np
from tomlkit import value
from tools import detect_pose_with_draw, BodyLandMarks
import mediapipe as mp
import json
from pathlib import Path
import yaml
layout = [[sg.Text('V-coach Execise Creator', size=(40, 1), justification='center', font='Helvetica 20',),sg.Text('Frame Count : ', size=(40, 1), justification='center', font='Helvetica 20',key="frame_count"),],
            [sg.Image(filename='', key='image'),sg.Listbox('',size=(30,30),key='listbox1',enable_events=True)],
            [sg.Image(filename='', key='image1')],
            [sg.Text('', size=(40, 1), justification='center', font='Helvetica 20',key="txt1"),],
            [sg.Text('Video Controls :', size=(40, 1), justification='center',font='Helvetica 20',border_width=0),sg.FileBrowse('Open Video File',file_types=(("Video Files", "*.mp4",),("Video Files","*.avi"),("Video Files","*.MOV"),),key="open"),sg.Button('Load Video', size=(10, 1), font='Helvetica 14'),
            sg.Button('Play Again', size=(10, 1), font='Any 14')],
            [sg.Text('Stage Edit :', size=(40, 1), justification='center'),sg.Button('Create Stage', size=(10, 1), font='Any 14',key='create_stage'),sg.Button('Finish and Write Stages', size=(10, 1), font='Any 14',key='finish'),sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]

enter_name_win_layout = [[sg.Text('Please Enter the name of execise you created:', size=(40, 1), justification='center', font='Helvetica 20',),sg.InputText(key="exe_name")],
                        [sg.Button('Submit', size=(10, 1), font='Any 14',key='submit'),sg.Button('Exit', size=(10, 1), font='Any 14',key='exit')]]


window = sg.Window('Demo Application - OpenCV Integration',
                    layout, location=(800, 400),return_keyboard_events=True)



video = False
pause = False
# reload = False

listboxone = []
stages_to_write = []
mp_pose = mp.solutions.pose
frame_count = 0
stage_count = 0

while True:
    event, values = window.read(timeout=10)
    if event == 'Exit' or event == sg.WIN_CLOSED or event == "Escape:9":
        window.close()
        cap.release()
        break
    
    if event == "open":
        window["txt1"].update(value="Press 'Load Video' button to loa the video.")

    if event == 'Load Video':
        video_path = values["open"]
        video = True
        pause = True
        cap = cv2.VideoCapture(video_path)
        # cap = cv2.VideoCapture("/home/thomasw/workspace/execise-creator-app/IMG_105610890.MOV")

    if event == 'Play Again':
        cap = cv2.VideoCapture(video_path)
        pause = True
        video = True

    if event == 'space:65':
        pause = bool(abs(1-int(pause)))
        sleep(1)

    if event == 'create_stage':
        lm = BodyLandMarks(results, mp_pose)
        stages_to_write.append(lm.return_all_points())
        print("Created stage {}".format(int(stage_count)))
        listboxone.append("Stage {}: Frame No. {}".format(str(stage_count),str(frame_count)))
        window['listbox1'].update(listboxone)
        stage_count+=1
        print(stages_to_write)

    if event == "finish":
        name_win = sg.Window("Enter Execise Name",enter_name_win_layout)
        while True:
            e,v = name_win.read()
            if e == "exit":
                name_win.close()
                break
            if e == "submit":
                wpath = sg.popup_get_folder(message="Please select the location to save the execise file.")
                try:
                    Path("{}/{}".format(wpath,v["exe_name"])).mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    tb=traceback.format_exc()
                    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)
                else:
                    stage_counter = 0
                    s = False
                    for i in range(len(stages_to_write)):
                        try:
                            with open("{}/{}/stage{}.json".format(wpath,v["exe_name"],str(i)),"w+",encoding="utf8") as f:
                                json.dump(stages_to_write[i],f)
                                f.close()
                        except Exception as e:
                            s = False
                            tb=traceback.format_exc()
                            sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)
                        else:
                            s = True
                    name_win.close()
                    with open("{}/{}/config.yaml".format(wpath,v["exe_name"]),"w+") as f:
                        yaml.dump({"stages_count":len(stages_to_write)})
                        f.close()
                    if s:
                        sg.popup_ok(title="Create Sucessful !")
                    else:
                        sg.popup_ok(title="Create Failed !")
                    break

        

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
        window["frame_count"].update(value="Frame Count : {}".format(str(frame_count)))
    else:
        window["txt1"].update(value="")
        frame_count = 0


