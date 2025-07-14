import ctypes
import sys
import os
# Installing pycaw screen-brightness-control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Volume control
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Brightness control
import screen_brightness_control as sbc

if sys.platform != 'win32':
    raise EnvironmentError("This script is intended to run on Windows only.")

def mute_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)
    except Exception as e:
        print(f"Failed to mute system: {e}")

def unmute_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)
    except Exception as e:
        print(f"Failed to unmute system: {e}")

def increase_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
        print("Volume increased")
    except Exception as e:
        print(f"Failed to increase volume: {e}")

def decrease_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
        print("Volume decreased")
    except Exception as e:
        print(f"Failed to decrease volume: {e}")

def increase_brightness():
    try:
        current = sbc.get_brightness(display=0)
        sbc.set_brightness(min(current[0] + 10, 100), display=0)
        print("Brightness increased")
    except Exception as e:
        print(f"Failed to increase brightness: {e}")

def decrease_brightness():
    try:
        current = sbc.get_brightness(display=0)
        sbc.set_brightness(max(current[0] - 10, 0), display=0)
        print("Brightness decreased")
    except Exception as e:
        print(f"Failed to decrease brightness: {e}")


def handle_wifi_bluetooth(query, speak):
    if ('turn on wifi' in query) or ('enable wifi' in query) or ('connect wifi' in query):
        try:
            os.system("netsh interface set interface Wi-Fi enabled")
            speak("WiFi enabled.")
        except Exception:
            speak("Sorry, I couldn't enable WiFi.")
    elif ('turn off wifi' in query) or ('disable wifi' in query) or ('disconnect wifi' in query):
        try:
            os.system("netsh interface set interface Wi-Fi disabled")
            speak("WiFi disabled.")
        except Exception:
            speak("Sorry, I couldn't disable WiFi.")
    elif ('turn on bluetooth' in query) or ('enable bluetooth' in query):
        try:
            os.system("powershell Start-Service bthserv")
            speak("Bluetooth enabled.")
        except Exception:
            speak("Sorry, I couldn't enable Bluetooth.")
    elif ('turn off bluetooth' in query) or ('disable bluetooth' in query):
        try:
            os.system("powershell Stop-Service bthserv")
            speak("Bluetooth disabled.")
        except Exception:
            speak("Sorry, I couldn't disable Bluetooth.")

def open_app(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "cmd": "cmd.exe",
        "explorer": os.path.expanduser("~"),
        "settings": "ms-settings:",
        "chatgpt": "ChatGPT.exe",
        "brave": "brave.exe"
    }
    if app_name in apps:
        os.startfile(apps[app_name])
        return f"Opening {app_name}."
    return "App not found."

def shutdown():
    os.system("shutdown /s /t 1")

def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")