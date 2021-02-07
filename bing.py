import os
import pickle
import random
import requests
import shutil
import pathlib
import ctypes
import sys

# Resolution 1920 or 1366
res = 1920
# Delete downloaded images or not
RemoveImg = True
# Network test variables
timeout = 10
url = 'http://www.google.com'
# Apply background
applyWall = True

markets = ['zh-CN', 'en-US', 'ja-JP', 'en-AU', 'en-UK', 'de-DE', 'en-NZ', 'en-CA']
network = False
# Check Interwebz
for attempt in range(10):
    try:
        _ = requests.get(url, timeout = 10)
    except requests.ConnectionError:
        print("PC isn't connected. Retrying...")
    else:
        print("PC is connected! Continuing...")
        network = True
        break

if network == False:
    print("Couldn't connect to the interwebs. Quitting...")
    sys.exit()

# What platform is this running from
from sys import platform
if platform == "linux" or platform == "linux2":
    platform = "linux"
    print("Warning! This platform is not completely supported. Only Gnome is completely supported (will apply wallpaper)")
elif platform == "darwin":
    platform = "macos"
    print("Warning! MacOS is currently not supported. The wallpaper will be downloaded but not applied. Support is almost planned. (I don't have a mac)")
elif platform == "win32":
    platform = "windows"
else:
    platform = "unknown"
    print("Warning! This platform is not supported, I don't even know what's the os.")

# Loading old_index
if os.path.isfile('bingvars.pickle'):
    with open('bingvars.pickle', 'rb') as f: 
        old_index, old_mkt_int = pickle.load(f)
else:
    old_index = 0
    old_mkt_int = 0

# Setting index and mkt and duplicate index and mkt prevention
while True:
    index = random.randint(1, 7)
    print("Old index: " + str(old_index))
    print("New index: " + str(index))

    if index != old_index:
        old_index = index
        print("Seems fine to me. Continuing...")
        
        # Now choose a market
        while True:
            mkt_int = random.randint(0,len(markets)-1)
            print("Old market: " + str(old_mkt_int) + " " + markets[old_mkt_int])
            print("New market: " + str(mkt_int) + " " + markets[mkt_int])

            if mkt_int != old_mkt_int:
                old_mkt_int = mkt_int
                print("Seems fine. Continuing...again...")

                with open('bingvars.pickle', 'wb') as f:
                    pickle.dump([old_index, old_mkt_int], f)
                break
            else:
                print("Why the same market? That's no good! Let's retry...")
        break
    else:  
        print("Those numbers seem the same. That's no good. Retring...")


# Get wall. Thanks to github user TimothyYe for the api (it's better than microsoft's)
BingWallURL = "https://bing.biturl.top/?format=image" + "&resolution=" + str(res) + "&index=" + str(index) + "&mkt=" + markets[mkt_int]
print("Got URL! " + BingWallURL)

filename = "BingDaily_res" + str(res) + "_index" + str(index) + "_mkt" + str(mkt_int) + "_" + markets[mkt_int] + ".jpg"
print("Filename is: " + filename)

getImage = requests.get(BingWallURL, stream = True)

if getImage.status_code == 200:
    getImage.raw.decode_content = True

    with open(filename, 'wb') as f:
        shutil.copyfileobj(getImage.raw, f)

    print('Image downloaded!1!!1')
else:
    print('Downloading failed successfully.')

# Setting Background
path = str(os.getcwd()) + '\\' + str(filename)

# big and complicated wall of codde to get platform and warn the user
if platform == "windows":
    if applyWall == False:
        print("I don't get it, why do you use me as a background downloader?")
        print("The wallpaper is here: " + path)
    else:
        print("Applying wallpaper...")
        print("Path: " + path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

elif platform == "linux":
    print("Gnome is currently the only supported DE for automatic wallpaper application.")
    if applyWall == False:
        print("I get it, you don't use Gnome, right?")
        print("The wallpaper is here: " + path)
    else:
        print("Applying wallpaper...")
        print("Path: " + path)
        cmd = "gsettings set org.gnome.desktop.background picture-uri file:" + path
        os.system(cmd)
else:
    print("Setting wallpaper isn't supported on this platform. Quitting...")
    sys.exit()

# Deleting image, if requested
if RemoveImg == True and applyWall == False:
    os.remove(path)
    sys.exit()
else:
    sys.exit()
