import mediapipe as mp

def file_read():
    '''
Select a file to read
    '''
    fp = ""
    #GUI layout
    layout = [
        [
            sg.FileBrowse(key="file"),
            sg.Text("File"),
            sg.InputText()
        ],
        [sg.Submit(key="submit"), sg.Cancel("Exit")]
    ]
    #WINDOW generation
    window = sg.Window("File selection", layout)
