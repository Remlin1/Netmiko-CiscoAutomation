from netmiko import ConnectHandler


#######################################################################################################################

# DEVICE LOGIN PARAMETERS CHANGE HERE
username = "automation"
password = "Z%P64Thjbu5&jMPy@8Z$5C35^"
device_type = "cisco_xe"

# FILE INPUT NAME CHANGE HERE
# Specify file name if saved in same directory as script, or specify direct filepath
device_import = "Switch_Device_List"
config_import = "SwitchConfigUpdate"

#######################################################################################################################


# Building Device List
device_file = open(device_import, "r")
device_list = [(line.rstrip()) for line in device_file]
device_file.close()

print(device_list)

# Building list of dictionaries for parameter reference
device_params = []
for device in device_list:
    params_dict = {
        "host": device,
        "username": username,
        "password": password,
        "device_type": device_type,
    }
    device_params.append(params_dict)

print(device_params)

# Importing Config File and building list of commands to push to device
cfg_file = open(config_import, "r")
cfg_list = [line.rstrip() for line in cfg_file]

print(cfg_list)

# Connecting to each device and running cfg file commands
for device in device_params:
    host_ip = list(device.values())[0]
    print("#" * 80)
    print(" "*21+" CONNECTING TO "+host_ip+" "*32)
    print("#" * 80)
    net_connect = ConnectHandler(**device)
    cfg_output = net_connect.send_config_set(cfg_list)
    print(cfg_output)

# cwd = os.getcwd()
# print(cwd)

