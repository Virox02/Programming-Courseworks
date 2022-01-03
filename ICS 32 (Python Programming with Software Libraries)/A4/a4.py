from pathlib import Path
from Profile import Profile, Post
from NaClProfile import NaClProfile
import os
import sys
import ds_client_a4
from OpenWeather import OpenWeather
from LastFM import LastFM
from ExtraCreditAPI import Bored

def input_user():
    print("--------------------------------------------------------------------------------")
    print("INPUT FORMAT --> [COMMAND] [INPUT] [[-]OPTION] [INPUT]")
    print("L - List the contents of the user specified directory")
    print(" => -r: Output directory content recursively\r\n => -f: Output only files, excluding directories in the results\r\n => -s: Output only files that match a given file name\r\n => -e: Output only files that match a give file extension")
    print("C - Create a new file in the specified directory(along with creating a profile, writing posts/bio)\r\nD - Delete the file\r\nR - Read the contents of a file(along with loading a profile, writing posts/bio)\r\nQ - Quit the program")
    print("---KEYWORDS---")
    print("@high -> High Temperature | @low -> Low Temperature | @temp -> Temperature \r\n@long -> Longitute | @lat -> Latitude | @weather -> Description | @city -> City\r\n@sunset -> Sunset Time | @hum -> Humidity")
    print("@top10 -> All top 10 artists | @lastfm -> Top artist | @top2 -> 2nd artist\r\n@top3 -> 3rd artist")
    print("@extracredit -> For an activity if you are bored")
    user = input().split()
    cmnd = user[0]
    ul = len(user)
    if cmnd == 'L':
        if len(user)<2:
            print('ERROR')
            funct()
        for j in range(-1, -(ul+1), -1):
            if '-r' in user:
                if user[j] == '-r':
                    rp = user[-(ul-1):j:+1]
            elif ('-s' in user) or ('-f' in user) or ('-e' in user):
                if user[j] == '-s' or user[j] == '-f' or user[j] == '-e':
                    rp = user[-(ul-1):j:+1]
            else:
                rp = user[1:ul:+1]
                opt = 'na'
                fnd = 'na'

        pl = len(rp)
        left_input = (ul) - (pl + 1)
            
        if left_input == 1:
            if user[-1] == '-r' or user[-1] == '-f':
                opt = user[-1]
                fnd = 'na'
            else:
                print('ERROR')
        elif left_input == 2:
            if user[-1] != '-f':
                opt = user[-2]
                fnd = user[-1]
            elif user[-1] == '-f' and user[-2] == '-r':
                opt = user[-2]+user[-1]
                fnd = 'na'
            else:
                print('ERROR')
        elif left_input == 3:
            if user[-2] == '-s' or user[-2] == '-e':
                opt = user[-3]+user[-2]
                fnd = user[-1]
            else:
                print('ERROR')
                
    elif cmnd == 'C':
        if len(user)<2:
            print('ERROR')
            funct()
        for j in range(-1, -(ul+1), -1):
            if '-n' in user:
                if user[j] == '-n':
                    rp = user[-(ul-1):j:+1]
        fnd = user[-1]
        opt = user[-2]
    elif cmnd == 'D':
        if len(user)<2:
            print('ERROR')
            funct()
        rp = user[1:ul:+1]
        opt = 'na'
        fnd = 'na'
    elif cmnd == 'R':
        if len(user)<2:
            print('ERROR')
            funct()
        rp = user[1:ul:+1]
        opt = 'na'
        fnd = 'na'

    elif cmnd == 'Q':
        if len(user)>1:
            print('ERROR')
            funct()
        rp = 'na'
        opt = 'na'
        fnd = 'na'

    else:
        print('ERROR')
        funct()
                    
    pt = ''
    for i in range(0, len(rp)-1):
        pt = pt+rp[i]+' '
    pt = pt+rp[-1]
        
    return cmnd, pt, opt, fnd

def funct():
    input_list = input_user()
    command = input_list[0]
    p = Path(input_list[1])
    option = input_list[2]
    find = input_list[3]
    fmapikey = "88f192fd5ff2f4231efea975e9e225ae"
    weatherapikey = "0940956a4df510aeb37bac0c7770841a"
    naclp = NaClProfile()
    keypair = naclp.keypair
    
    if command == 'L':
        if len(input_list)<2:
            print('ERROR')
            funct()
        else:
            if option == 'na' and find == 'na':
                contents = p.iterdir()
                sor_con = sorted(contents)
                for c in sor_con:
                    if c.is_file():
                        print(c)
                for c in sor_con:
                    if c.is_dir():
                        print(c)
        
            elif (option == '-f' or option == '-r-f') and find == 'na':
                 rf_option(p, option)
                 
            elif option == '-r' and find == 'na':
                 r(p)
                 
            elif option == '-r-s' or option == '-s':
                r_s(p, option, find)
                
            elif option == '-r-e' or option == '-e':
                re_option(p, option, find)

            else:
                print('ERROR')
                funct()
            
    elif command == 'C':
        if len(input_list)<4:
            print('ERROR')
            funct()
        else:
            dsu_path = C_command(p, find)
            print(dsu_path, "created")
            print("Please enter your profile information")
            username = input("Please enter your username")
            password = input("Please enter your password")
            dsuserver = input("Please enter the dsuserver")
            lastfm = LastFM(fmapikey) #assigning LastFM class to an object #apikey is hardcoded at the start 
            openweather = OpenWeather(weatherapikey, "92697", "US") #assigning OpenWeather class to an object #apikey is hardcoded at the start
            bored = Bored() #assigning Bored class to an object. This API does not require any apikey or argument
            pro = NaClProfile() #assigning Profile class to an object
            pro.username = username
            pro.password = password
            pro.dsuserver = dsuserver
            print("WARNING! IF YOU CHOOSE TO ENTER A POST OR BIO, IT WILL AUTOMATICALLY BE PUBLISHED ON THE SERVER") #warning the user about posting
            yn = input("Do you want to enter a bio? (yes/no)") #if user wants to add a bio
            if yn == 'yes':
                bio = input("Please enter your bio")
                pro.bio = bio
                bio_post = Post(entry = bio) #adding a bio
            else:
                if yn != 'no':
                    print("invalid input")
                    funct()
            yn_2 = input("Do you want to write a post? (yes/no)") #if user wants to add a post
            if yn_2 == 'yes':
                post_msg = input("Please enter the message for the post")
                if ('@high' in post_msg) or ('@low' in post_msg) or ('@sunset' in post_msg) or ('@temp' in post_msg) or ('@long' in post_msg) or ('@lat' in post_msg) or ('@weather' in post_msg) or ('@hum' in post_msg) or ('@city' in post_msg):
                    post_msg = openweather.transclude(post_msg) #transcluding the post message (openweather)
                if ('@lastfm' in post_msg) or ('@top2' in post_msg) or ('@top3' in post_msg) or ('@top10' in post_msg):
                    post_msg = lastfm.transclude(post_msg) #transcluding the post message (lastfm)
                if '@extracredit' in post_msg:
                    post_msg = bored.transclude(post_msg)#transcluding the post message (extracredit api)
                post = Post(entry = post_msg) #adding a post
                pro.add_post(post)
            else:
                if yn_2 != 'no':
                    print("invalid input")
                    funct()
            pro.save_profile(str(dsu_path))
            if yn == 'yes' and yn_2 == 'yes':
                ds_client_a4.send(keypair, dsuserver, 2021, username, password, post_msg, bio) #sending to client with bio
            elif yn == 'no' and yn_2 == 'yes':
                ds_client_a4.send(keypair, dsuserver, 2021, username, password, post_msg) #sending to client without bio
            
            
            

    elif command == 'D':
        if len(input_list)<2:
            print('ERROR')
            funct()
        else:
            D_command(p)

    elif command == 'R':
        if len(input_list)<2:
            print('ERROR')
            funct()
        else:
            R_command(p)
            print("")
            yn = input("Do you want to load the existing file? (yes/no)") #if user wants to load an existing file
            if yn == 'yes':
                lastfm = LastFM(fmapikey) #assigning LastFM class to an object #apikey is hardcoded at the start 
                openweather = OpenWeather(weatherapikey, "92697", "US") #assigning OpenWeather class to an object #apikey is hardcoded at the start 
                bored = Bored() #assigning Bored class to an object. This API does not require any apikey or argument
                p2 = NaClProfile() #assigning Profile class to an object
                p2.load_profile(str(p))
                print("WARNING! IF YOU CHOOSE TO ENTER A POST OR BIO, IT WILL AUTOMATICALLY BE PUBLISHED ON THE SERVER")
                yn_2 = input("Do you want to add a bio? (yes/no)") #asking if user wants to ass a bio
                if yn_2 == 'yes':
                    bio = input("Please enter your bio")
                    p2.bio = bio
                    bio_post = Post(entry = bio) #adding a bio
                else:
                    if yn_2 != 'no':
                        print("invalid input")
                        funct()
                yn_3 = input("Do you want to add a post? (yes/no)") #asking if user wants to add a post
                if yn_3 == 'yes':
                    post_msg = input("Please enter the message for the post")
                    if ('@high' in post_msg) or ('@low' in post_msg) or ('@sunset' in post_msg) or ('@temp' in post_msg) or ('@long' in post_msg) or ('@lat' in post_msg) or ('@weather' in post_msg) or ('@hum' in post_msg) or ('@city' in post_msg):
                        post_msg = openweather.transclude(post_msg) #transcluding the post mssg (openweather)
                    if ('@lastfm' in post_msg) or ('@top2' in post_msg) or ('@top3' in post_msg) or ('@top10' in post_msg):
                        post_msg = lastfm.transclude(post_msg) #transcluding the post mssg (lastfm)
                    if '@extracredit' in post_msg:
                        post_msg = bored.transclude(post_msg) #transcluding the post mssg (extracredit api)
                    post = Post(entry = post_msg) #adding a post
                    #print(post)
                    p2.add_post(post)
                else:
                    if yn_3 != 'no':
                        print("invalid input")
                        funct()
                p2.save_profile(str(p))
                if yn_2 == 'yes' and yn_3 == 'yes':
                    ds_client_a4.send(keypair, str(p2.dsuserver), 2021, str(p2.username), str(p2.password), post_msg, bio) #seding to client with bio
                elif yn_2 == 'no' and yn_3 == 'yes':
                    ds_client_a4.send(keypair, str(p2.dsuserver), 2021, str(p2.username), str(p2.password), post_msg) #sending to client wihtout bio
            else:
                if yn != 'no':
                    print("invalid input")
                    funct()
            

    if command == 'Q':
        sys.exit()
    else:
        funct()

    

def f_option(path):
    contents = path.iterdir()
    sor_con = sorted(contents)
    for c in sor_con:
        if c.is_file():
            print(c)
            
def rf_option(path, option):
    contents = path.iterdir()
    sor_con = sorted(contents)
    if option == '-f':
        for c in sor_con:
            if c.is_file():
                print(c)
    elif option == '-r-f':
        for c in sor_con:
            if c.is_file():
                print(c)
        for c in sor_con:
            if c.is_dir():
                rf_option(c, option)

def r(path):
    contents = path.iterdir()
    sor_con = sorted(contents)
    for c in sor_con:
        if c.is_file():
            print(c)
    for c in sor_con:
        if c.is_dir():
            print(c)
            r(c)

def s_option(find, path):
    contents = path.iterdir()
    sor_con = sorted(contents)
    for c in sor_con:
        if c.is_file():
            if find == c.name:
                print(c)
    
def r_s(path, option, find):
    contents = path.iterdir()
    sor_con = sorted(contents)
    if option == '-s':
        for c in sor_con:
            if c.is_file():
                if find == c.name:
                    print(c)
    elif option == '-r-s':
        for c in sor_con:
            if c.is_file():
                if find == c.name:
                    print(c)
        for c in sor_con:
            if c.is_dir():
                r_s(c, option, find)
            

def re_option(path, option, find):
    contents = path.iterdir()
    sor_con = sorted(contents)
    if option == '-r-e':
        for c in list(path.glob('**/*.{}'.format(find))):
            print(c)
    elif option == '-e':
        for c in list(path.glob('*.{}'.format(find))):
            print(c)

def C_command(path, name):
    filename = name+'.dsu'
    pth = str(path)
    pth = pth+'//'+filename
    p = Path(pth)
    if os.path.exists(p):
        print("ERROR.... The file already exists!")
        funct()
    else:
        file = open(p, "w")
        file.write("")
        file.close()
        return p

def D_command(path):
    pth = str(path)
    p_th = pth.split('.')
    if p_th[-1] == 'dsu':
        os.remove(path)
        print(pth, 'DELETED')
    else:
        print('ERROR')
        funct()
        
def R_command(pth):
    pth = str(pth)
    p_th = pth.split('.')
    if p_th[-1] == 'dsu':
        if os.path.getsize(pth) == 0:
            print('EMPTY')
        else:
            file = open(pth, "r")
            f_contents = file.read()
            file.close()
            print(f_contents, end='')
    else:
        print('ERROR')
        funct()
        
            
if __name__ == "__main__":
    funct()
