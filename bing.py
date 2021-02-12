import os
import pickle
import random
import requests
import shutil
import pathlib
import ctypes
import sys

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

# FUNctions ahah
def first_time_here():
    print("It seems you haven't used this thing yet...")
    print("It's time for a first time setup! Don't worry it won't take long but you have to restart the script after the setup is done.")
    step = 1

    while step == 1:
        print()
        res = input("Do you prefer HD (1366) or FullHD (1920) images? ")
        print(str(res))
        if str(res) == "1920":
            print("FullHD it is.")
            res = 1920
            step = 2
            break
        elif str(res) == "1366":
            print("HD it is.")
            step = 2
            res = 1366
            break
        else:
            print("Sorry i didn't understand that.")
            print("You can type 1366 HD images.")
            print("You can type 1920 FullHD images.")
            print()
            print("Let's retry.")

    while step == 2:
        print()
        applyWall = input("Do you want me to apply the images after I download them? (Y/N) ")
        if applyWall.casefold() == "y":
            print("Ok. Remember that if I don't recognize the OS or the DE I won't apply it.")
            applyWall = True
            step = 3
            break
        elif applyWall.casefold() == "n":
            print("Ok. I'm not going to apply any wallpaper.")
            applyWall = False
            step = 3
            break
        else:
            print("I'm sorry but I need a yes or no answer here.")
            print("Let's retry.")


    while step == 3:
        print()
        RemoveImg = input("Do you want me to remove the images after I apply them? (Y/N) ")
        if RemoveImg.casefold() == "y":
            print("Yay, I get to use my new vaccumm cleaner!")
            RemoveImg = True
            step = 4
            break
        elif RemoveImg.casefold() == "n":
            print("Oh, ok.")
            RemoveImg = False
            step = 4 
            break
        else:
            print("I'm sorry but I need a yes or no answer here.")
            print("Let's retry.")

    while step == 4:
        Desktop = 9999
        fehoption = 9999
        if platform == "linux" and applyWall == True:
            print()
            print("What DE are you using?")
            print("1 - Gnome")
            print("2 - Mate")
            print("3 - Cinnamon")
            print("0 - Other (use feh to apply wallpaper)")
            Desktop = input("0-3? ")

            if Desktop != 1 or 2 or 3 or 0:
                print("Please choose an option.")
                print()
                print("Let's retry.")
            else:
                step = 5
                break
        else:
            break
    
    while step == 5:
        if Desktop == 0:
            print()
            print("Remember to install feh")
            fehoption = input("Choose between --bg-fill, --bg-max, --bg-scale or --bg-tile. ")

            if fehoption != "--bg-fill" or "--bg-max" or "--bg-scale" or "--bg-tile":
                print("Please type --bg-max, --bg-max, --bg-scale or --bg-tile.")
                print()
                print("Let's retry.")
            else:
                break
        else:
            break
    
    old_index = 0
    old_mkt_int = 0
    
    print("Thanks for your time, saving info...")
    with open('brdwvars.pickle', 'wb') as f:
        pickle.dump([old_index, old_mkt_int, res, applyWall, RemoveImg, Desktop, fehoption], f)
    sys.exit()

# Network test variable
url = 'http://www.google.com'
markets = ['zh-CN', 'en-US', 'ja-JP', 'en-AU', 'en-UK', 'de-DE', 'en-NZ', 'en-CA']
network = False

# Check Interwebz
for attempt in range(10):
    try:
        _ = requests.get(url, timeout = 10)
    except requests.ConnectionError:
        print("PC isn't connected to the internet. Retrying...")
    else:
        print("PC is connected to the internet! Continuing...")
        network = True
        break

if network == False:
    print("Couldn't connect to the interwebs. Quitting...")
    sys.exit()

# Loading variables or running intial setup
if os.path.isfile('brdwvars.pickle'):
    with open('brdwvars.pickle', 'rb') as f: 
        old_index, old_mkt_int, res, applyWall, RemoveImg, Desktop, fehoption = pickle.load(f)
else:
    first_time_here()

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
else:
    print("Setting wallpaper isn't supported on this platform. Quitting...")
    sys.exit()

# Deleting image, if requested
if RemoveImg == True and applyWall == False:
    os.remove(path)
    sys.exit()
else:
    sys.exit()
