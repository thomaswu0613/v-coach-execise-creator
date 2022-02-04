import PySimpleGUI as sg

# Functions
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




layout = [[sg.Button('Ok'), sg.Button('Cancel')] ]

window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()
    print("events:")
    print(event)
    print("values:")
    print(values)
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "Hello":
        file_read()
    
    

window.close()