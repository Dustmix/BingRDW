#!/usr/bin/env python

import os
import pickle
import random
import requests
import shutil
import pathlib
import ctypes
import sys
from fun import update, first_time_here

netTestUrl = 'http://www.google.com'
markets = ['zh-CN', 'en-US', 'ja-JP', 'en-AU', 'en-UK', 'de-DE', 'en-NZ', 'en-CA']
disableAutoUpdates = False

# What platform is this running from
if sys.platform == "linux" or sys.platform == "linux2":
    platform = "linux"
    print("Warning! This platform is not completely supported. Check the readme on the Github page for more info.")
elif sys.platform == "darwin":
    platform = "macos"
    print("Warning! MacOS is currently not supported. The wallpaper will be downloaded but not applied. (I don't have a mac)")
elif sys.platform == "win32":
    platform = "windows"
else:
    platform = "unknown"
    print("Warning! This platform is not supported, I don't even know what's the os.")

# Check Interwebz
while True: # I put it as an infinite loop because this program is ment to be run on a schedule everyday so it retrys until it find a connection
    try:
        _ = requests.get(netTestUrl, str(10))
    except requests.ConnectionError:
        print("PC isn't connected to the internet. Retrying...")
    else:
        print("PC is connected to the internet! Continuing...")
        if disableAutoUpdates == True:
            print("Autoupdates are disabled! If this is a bug or the updates create a bug please report this in the issues tab in the github page")
        else:
            update(os.path.basename(__file__))
        break

# Loading variables or running intial setup
if os.path.isfile('brdwvars.pickle'):
    with open('brdwvars.pickle', 'rb') as f: 
        old_index, old_mkt_int, res, applyWall, RemoveImg, Desktop, fehoption = pickle.load(f)
else:
    first_time_here(platform=platform)
    sys.exit()

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

                with open('brdwvars.pickle', 'wb') as f:
                    pickle.dump([old_index, old_mkt_int, res, applyWall, RemoveImg, Desktop, fehoption], f)
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
    print('Download failed successfully.')

# Setting Background
path = str(os.getcwd()) + '\\' + str(filename)

# big and complicated wall of code to get platform and warn the user
if platform == "windows":
    if applyWall == False:
        print("The wallpaper is here: " + path)
    else:
        print("Applying wallpaper...")
        print("Path: " + path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        if RemoveImg == True: # Deleting image, if requested
            os.remove(path)
        sys.exit()

elif platform == "linux":
    if applyWall == False:
        print("The wallpaper is here: " + path)
    else:
        print("Applying wallpaper...")
        print("Path: " + path)
        if Desktop == 1:
            cmd = "gsettings set org.gnome.desktop.background picture-uri file:" + path
            os.system(cmd)
        elif Desktop == 2:
            cmd = "gsettings set org.mate.background picture-filename file:" + path
            os.system(cmd)
        elif Desktop == 3:
            cmd = "gsettings set org.cinnamon.desktop.background picture-uri file:" + path
            os.system(cmd)
        elif Desktop == 0:
            cmd = "feh " + fehoption + " " + path
            os.system(cmd)
        if RemoveImg == True: # Deleting image, if requested
            os.remove(path)
        sys.exit()
else:
    print("Setting wallpaper isn't supported on this platform. Quitting...")
    sys.exit()
