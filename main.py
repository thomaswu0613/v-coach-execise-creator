import os
import traceback
from pathlib import Path
import PySimpleGUI as sg
import cv2
import numpy as np
from tools import detect_pose_with_draw, BodyLandMarks
import mediapipe as mp
import yaml
from shutil import copyfile
import subprocess, shlex

def submit_layout():
    return [[sg.Text('Please Enter the name of execise you created:', size=(60, 1), justification='center', font='Helvetica 20',key="txt3"),sg.InputText(key="exe_name")],
                        [sg.Text('Please Select the path where you want to save the files:', size=(60, 1), justification='center', font='Helvetica 20',key="txt4"),sg.InputText(key="exe_name"),sg.FolderBrowse('Select Folder',key='select_folder')],
                        [sg.Button('Submit', size=(10, 1), font='Any 14',key='submit'),sg.Button('Quit Program', size=(15, 1), font='Any 14',key="quit"),sg.Button('Close this dialog and continue', size=(30, 1), font='Any 14',key="exit")]]


layout = [[sg.Text('V-coach Execise Creator', size=(40, 1), justification='center', font='Helvetica 20',),sg.Text('Frame Count : ', size=(40, 1), justification='center', font='Helvetica 20',key="frame_count"),],
            [sg.Image(filename='', key='image'),sg.Listbox('',size=(30,30),key='listbox1',enable_events=True)],
            [sg.Image(filename='', key='image1')],
            [sg.Text('', size=(40, 1), justification='center', font='Helvetica 20',key="txt1"),],
            [sg.Text('Video Controls :', size=(60, 1), justification='center',font='Helvetica 20',border_width=0),sg.FileBrowse('Open Video File',file_types=(("Video Files", "*.mp4",),("Video Files","*.avi"),("Video Files","*.MOV"),),key="open"),sg.Button('Load Video', size=(10, 1), font='Helvetica 14'),
            sg.Button('Play Again', size=(10, 1), font='Any 14')],
            [sg.Text('Stage Edit :', size=(60, 1), justification='center'),sg.Button('Create Stage', size=(15, 1), font='Any 14',key='create_stage',visible=False),sg.Button('Finish and Write Stages', size=(25, 1), font='Any 14',key='finish'),sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]

window = sg.Window('V-coach Execise Creator',
                    layout, location=(800, 400),return_keyboard_events=True)



video = False
pause = False
wait = False
processing = False
ready = False

listboxone = []
stages_to_write = []
mp_pose = mp.solutions.pose
frame_count = 0
stage_count = 1
scoring_lib_dir = "/home/thomasw/workspace/v-coach-pose-training-app/scoring_lib"
python_path = "/home/thomasw/anaconda3/bin/python"

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

    if event == 'create_stage':
        lm = BodyLandMarks(results, mp_pose)
        stages_to_write.append(lm.return_all_points())
        listboxone.append("Stage {}: Frame No. {}".format(str(stage_count),str(frame_count)))
        window['listbox1'].update(listboxone)
        stage_count+=1

    if event == "finish":
        submit_window = sg.Window("Enter Execise Name",submit_layout())

        while True:
            e,v = submit_window.read(timeout=20)
            if e == "exit":
                submit_window.close()
                break
            if e == "quit":
                submit_window.close()
                window.close()
                break
            if e == "submit" or wait is True:
                try:
                    if wait is False:
                        path_to_create = "{}/{}".format(v["select_folder"],v["exe_name"])
                        os.makedirs(path_to_create, exist_ok=False)
                        nom_path = os.path.normpath(video_path)
                        path_com = nom_path.split(os.sep)
                        copyfile(video_path,str(path_to_create+"/{}".format(path_com[-1])))
                        with open("{}/stages.yaml".format(path_to_create),"w+") as f:
                            for i in range(len(stages_to_write)):
                                yaml.dump({'stage{}'.format(i+1):stages_to_write[i]},f)
                        with open("{}/config.yaml".format(path_to_create),"w+") as f:
                            yaml.dump({'max_stages':len(stages_to_write)},f )
                    wait = True
                    args = shlex.split("{}/keypoints_from_video.py --activity {} --video {} --lookup {}/lookup_{}.pickle".format(scoring_lib_dir,v["exe_name"],video_path,path_to_create,v["exe_name"]))
                    if processing is False:
                        p=subprocess.Popen(args,stdout=subprocess.PIPE)
                        processing = True
                    out, err = p.communicate(input=None, timeout=None)
                    if p.poll() is None:
                        wait = True
                        processing = True
                        continue
                    else: 
                        if "Lookup Table Created" in out.decode():
                            sg.popup_ok("Creation Success!")
                            p.close()
                        else:
                            sg.popup_error("Create Failed!")
                except FileExistsError:
                    sg.popup_error("Folder Exists! Please rename your execise.")
                except Exception as e:
                    tb=traceback.format_exc()
                    sg.popup_error("Error!",e,tb)
                else:
                    sg.popup_ok("Creation Success!")
        

    if video:
        window["create_stage"].update(visible=True)
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
        window["create_stage"].update(visible=False)
        frame_count = 0
        video = False

