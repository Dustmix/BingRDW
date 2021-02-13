import os
import requests
import pickle
import requests
import hashlib
import shutil
import sys

def file_as_bytes(file):
    with file:
        return file.read()

# FUNction (I hate this)
def first_time_here(platform):
    print("It seems you haven't used this thing yet...")
    print("It's time for a first time setup! Don't worry it won't take long but you have to restart the script after the setup is done.")
    step = 1

    while step == 1:
        print()
        res = input("Do you prefer HD (1366) or FullHD (1920) images? ")
        print(str(res))
        if str(res) == "1920":
            print("FullHD it is.")
            step = 2
            break
        elif str(res) == "1366":
            print("HD it is.")
            step = 2
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

def update(fname):
    # Download a new sha256
    repo = "https://raw.githubusercontent.com/Dustmix/BingRDW/main"
    newfname = fname + "_new.py"
    funame = os.path.basename(__file__)
    newfuname = funame + "_new.py"

    r = requests.get(repo + "/SHA256", stream = True)
    if r.status_code == 200:
        new_py_sha256, new_fun_sha256 = r.text.splitlines()

    # Get and check current sha256
    old_sha256 = hashlib.sha256(file_as_bytes(open(fname, 'rb'))).hexdigest()

    # Compare sha256
    if old_sha256.casefold() != new_py_sha256.casefold():
        print("Found a new update! Updating...")
        # Updating begins now.
        r = requests.get(repo + "/BingRDW.py", stream = True)
        # Download 1/2
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(newfname, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                f.close()
            # Compare 1/2
                old_sha256 = hashlib.sha256(file_as_bytes(open(newfname, 'rb'))).hexdigest()
                
                if old_sha256.casefold() == new_py_sha256.casefold():
                    print("Download successful! (1/2)")
                    # Download 2/2
                    r = requests.get(repo + "/fun.py", stream = True)
                    
                    if r.status_code == 200:
                        r.raw.decode_content = True
                        with open(newfuname, 'wb') as f:
                            shutil.copyfileobj(r.raw, f)
                            f.close()
                        # Compare 2/2
                        old_sha256 = hashlib.sha256(file_as_bytes(open(newfuname, 'rb'))).hexdigest()

                        if old_sha256.casefold() == new_fun_sha256.casefold():
                            print("Download successful! (2/2)")
                            print("Great! Continuing update...")
                            os.remove(fname)
                            os.rename(newfname, fname)
                            print("Update successful! (1/2)")
                            os.remove(funame)
                            os.rename(newfuname, funame)
                            print("Update successful! (2/2)")
                            print("Great! Restarting....")
                            os.execl(sys.executable, sys.executable, *sys.argv)
                        else:
                            print("Download failed. Skipping update...")
                            os.remove(newfname)
                            return
                else:
                    print("Download failed. Skipping update...")
                    os.remove(newfname)
                    return
    else:
        print("No update found.")

    
