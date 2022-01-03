from pathlib import Path
import os


def function():
    input_list = input_user()
    command = input_list[0]
    p = Path(input_user[1])
    option = input_user[2]
    find = input_user[3]
    if command == 'L':
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
            function()
            
    elif command == 'C':
        C_command(p, find)

    elif command == 'D':
        D_command(p)

    elif command == 'R':
        R_command(p)

    elif command == 'Q':
        break
    
    else:
        print('ERROR')
        function()
    
        
            
def C_command(path, name):
    filename = name+'.dsu'
    pth = str(path)
    pth = pth+'\\'+filename
    p = Path(pth)
    file = open(p, "w")
    file.write("")
    file.close()
    print(p)

def D_command(path):
    pth = str(path)
    p_th = pth.split('.')
    if p_th[-1] == 'dsu':
        os.remove(path)
        print(pth, 'DELETED')
    else:
        print('ERROR')
        function()
        
def R_command(pth):
    if os.path.getsize(pth) == 0:
        print('EMPTY')
    else:
        file = open(pth, "r")
        f_contents = file.read()
        file.close()
        print(f_contents)
    


def v():
    contents = p.iterdir()
    sor_con = sorted(contents)
    for c in list(p.glob('**/*.{}'.format(find))):
        print(c)

def s_option():
    file = []
    contents = p.iterdir()
    sor_con = sorted(contents)
    for c in sor_con:
        if c.is_file():
            if find == c.name:
                print(c)

def r(p):
    contents = p.iterdir()
    sor_con = sorted(contents)
    for c in sor_con:
        if c.is_file():
            print(c)
    for c in sor_con:
        if c.is_dir():
            print(c)
            r(c)
def r_s(p):
    contents = p.iterdir()
    sor_con = sorted(contents)
    for c in sor_con:
        if c.is_file():
            if find == c.name:
                print(c)
    for c in sor_con:
        if c.is_dir():
            r_s(c)

def listing(v):
    cntnts = v.iterdir()
    s_c = sorted(cntnts)
    for i in s_c:
        if i.is_file():
            print(i)
    for i in s_c:
        if i.is_dir():
            print(i)

def exists():
    contents = p.iterdir()
    sor_con = sorted(contents)
    if Path(find).is_file():                                                                    
        print('yes')

def exten(p):
    for f in os.listdir(p):
        if os.path.isfile(f) and f.endswith(".{}".format(find)):
            print(f)

def exten_r(p):
    for f in os.listdir(p):
        if os.path.isfile(os.path.join('.', f)) and f.endswith(find):
            print(f)
    for f in os.listdir(p):
        if os.path.isdir(f):
            exten_r(f)


#def input():
 #   user = input().split()
  #  user[1:3]

# L C:\Users\Viraj\Desktop\Tes ta1 -r txt




#user = input("[COMMAND] [INPUT] [[-]OPTION] [INPUT]").split()
#command = user[0]
#p = Path(user[1])


def input_user():
    user = input("[COMMAND] [INPUT] [[-]OPTION] [INPUT]").split()
    cmnd = user[0]
    ul = len(user)
    if cmnd == 'L':
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
        else:
            print('ERROR')
    elif cmnd == 'C':
        for j in range(-1, -(ul+1), -1):
            if '-n' in user:
                if user[j] == '-n':
                    rp = user[-(ul-1):j:+1]
        user[-1] = fnd
        user[-2] = opt
    elif cmnd == 'D':
        rp = user[1:ul:+1]
        opt = 'na'
        fnd = 'na'
    elif cmnd == 'R':
        rp = user[1:ul:+1]
        opt = 'na'
        fnd = 'na'
                    
    pt = ''
    for i in rp:
        pt = pt+i
        
    return cmnd, pt, opt, fnd


        
            
            
            
                    
        

find = user[-1]

v()
