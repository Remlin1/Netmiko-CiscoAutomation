import PySimpleGUI as sg
from netmiko import ConnectHandler

#Theme
sg.theme('DarkBlue16')

#File Input Row1/Column1
file_input = [
    [
        sg.Text("Device List File",font = ('Calibri', 12)),
        sg.In(size=(100, 5), key="-DEVICE FILE-"),
        sg.FileBrowse(),
        sg.Button("View",size=(15,1)),

    ],

    [
        sg.Text("Config File",font = ('Calibri', 12)),
        sg.In(size=(104, 5), key="-CONFIG FILE-"),
        sg.FileBrowse(),
        sg.Button("Run",size=(15,1))
    ],
]

# Credentials Input Row1/Column2
credentials = [
    [
        sg.Text("Username", font=('Calibri', 12)),
        sg.In(size=(80, 5), key="-USERNAME-"),
    ],
    [
        sg.Text("Password", font=('Calibri', 12)),
        sg.In(size=(81, 5), key="-PASSWORD-",password_char='*'),
    ],
]

# Device List Row2,Column1
device_list_column = [
    [
        sg.Text("Device List",font = ('Calibri', 18))
    ],


    [
        sg.Listbox(values =[''], size = (50, 40),font = ('Calibri', 12), background_color ='White',key = '_deviceDisplay_', text_color='Black')
    ]
]
# Command list Row2,Column2
config_list_column = [
    [
        sg.Text("Commands To Run",font = ('Calibri', 18))
    ],

    [
        sg.Listbox(values =[''], size = (75, 40),font = ('Calibri', 12), background_color ='White',key = '_configDisplay_', text_color='Black')
    ]
]


# Output Text Ro2,Column3
output_column= [
    [
        sg.Text("Device Output", font=('Calibri', 18))
    ],
    [
        sg.Output(size=(100,50))
     ],

]

trademark = [
    [
        sg.Text("Created by Ross Barnett, Senior Infrastructure Intern", font=('Calibri', 6))
    ]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_input),
        sg.VSeperator(),
        sg.Column(credentials),
     ],

    [
        sg.Column(device_list_column),
        sg.VSeperator(),
        sg.Column(config_list_column),
        sg.VSeperator(),
        sg.Column(output_column),
    ],
    [
        trademark
    ]
]

#Build Window
window = sg.Window("Cisco Device Automation", layout, resizable=True).Finalize()


# Run the Event Loop
while True:
    event,values = window.read()

    # display device list
    def device_list(list):

        global device_list_displayed
        device_list_displayed = list
        # add list elements with new line
        values_device = [l for l in list]
        window.find_element('_deviceDisplay_').Update(values_device)

    # display config list
    def config_list(list2):

        global config_list_displayed
        config_list_displayed = list2
        # add list elements with new line
        values_config = [l for l in list2]
        window.find_element('_configDisplay_').Update(values_config)

    # Populates Device and Command Output when view is clicked
    if event == 'View':

        if values['-DEVICE FILE-'] == "" or values['-CONFIG FILE-'] == "":
            sg.popup('Please select a device and config file!')

        else:
            device_filepath = str(values["-DEVICE FILE-"])
            config_filepath = str(values["-CONFIG FILE-"])

            devices = [line.strip() for line in open(device_filepath)]
            config = [line.strip() for line in open(config_filepath)]

            device_list(devices)
            config_list(config)


    # Applies configuration commands when run button is clicked
    elif event == 'Run':
        if values['-DEVICE FILE-'] == "" or values['-CONFIG FILE-'] == "":
            sg.popup('Please select a device and config file!')
        else:
            username = str(values["-USERNAME-"])
            password = str(values["-PASSWORD-"])
            device_type = "cisco_xe"
            device_import = str(values["-DEVICE FILE-"])
            config_import = str(values["-CONFIG FILE-"])

            # Building Device List
            device_file = open(device_import, "r")
            device_listR = [(line.rstrip()) for line in device_file]
            device_file.close()



            # Building list of dictionaries for parameter reference
            device_params = []
            for device in device_listR:
                params_dict = {
                    "host": device,
                    "username": username,
                    "password": password,
                    "device_type": device_type,
                }
                device_params.append(params_dict)



            # Importing Config File and building list of commands to push to device
            cfg_file = open(config_import, "r")
            cfg_list = [line.rstrip() for line in cfg_file]
            cfg_file.close()


            # Connecting to each device and running cfg file commands
            for device in device_params:
                host_ip = list(device.values())[0]
                print("#" * 60)
                print(" CONNECTING TO " + host_ip)
                print("#" * 60)
                window.Refresh()
                net_connect = ConnectHandler(**device)
                cfg_output = net_connect.send_config_set(cfg_list)
                net_connect.save_config()
                print(cfg_output)
                window.Refresh()

    if event == sg.WIN_CLOSED:
        break


window.close()