# -*- coding: utf-8 -*-
from core.messq import *
import subprocess, requests
import os, stat
import shutil
import random,string

Rabbithost = '10.0.20.11'
Rabbituser = 'n1ctf'
Rabbitpass = 'b5d608c6d61'
waf_file = "/var/www/html/waf.php"

def randstr():
    rand_s = "".join(random.sample(string.ascii_letters+string.digits,random.randint(0,9)))
    return bytes(rand_s, encoding = "utf8")

def check():
    win = 0
    nowebshell = os.listdir("../cases/nowebshell-case")
    webshell = os.listdir("../cases/webshell-case")
    checklist = nowebshell + webshell
    random.shuffle(checklist)
    url = "http://127.0.0.1/waf.php"
    for check_file in checklist:
        if check_file[0] == 'n':
            case = open('../cases/nowebshell-case/'+check_file,'rb').read()
            case = randstr() + case
            res = requests.post(url=url,data=case,timeout=2)
            print(res.text)
            if res.text == "no-webshell":
                win += 1
                continue
            else:
                continue
        else:
            case = open('../cases/webshell-case/'+check_file,'rb').read()
            case = randstr() + case
            res = requests.post(url=url,data=case,timeout=2)
            print(res.text)
            if res.text == "webshell":
                win += 1
            else:
                continue
    return win
while True:
    expexecQ = MessageQ(Rabbithost,Rabbituser,Rabbitpass,'playerwaf')
    resQ = MessageQ(Rabbithost,Rabbituser,Rabbitpass,'result')
    waf = expexecQ.recv()
    print(waf)
    waf = json.loads(waf)
    if waf['waf'] != "":
        waf_tmp = open('waf_tmp','wb')
        waf_tmp.write(bytes(waf['waf'],'utf8'))
        waf_tmp.close()
        ret = subprocess.Popen('php -f check_waf.php', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        if ret.stdout.readline() == b"check ok": 
            shutil.move("waf_tmp",waf_file)
            os.chmod(waf_file,stat.S_IRWXO|stat.S_IRWXG|stat.S_IRWXU)
            res = check()
            try:
                os.remove(waf_file)
            except:
                res = 0
            nowebshell = os.listdir("../cases/nowebshell-case")
            webshell = os.listdir("../cases/webshell-case")
            checklist = nowebshell + webshell
            all_c = len(checklist)
            result = json.dumps({"team":waf['user'],"score":str(res)})
            resQ.send(result)
            '''
            if res == all_c:
                #result = json.dumps({"mail":waf['user'],"res":"Congratulations, you are the master of waf! :)\n Flag is : "+flag})
                result = json.dumps({"team":waf['user'],"score":})
                print(result)
                resQ.send(result)
            else:
                result = json.dumps({"mail":waf['user'],"res":"Your waf is not very suitable.\nYour score: "+str(res)+"/"+str(all_c)})
                print(result)
                resQ.send(result)
            '''
        else:
            os.remove("waf_tmp")
            #result = json.dumps({"mail":waf['user'],"res":"Please check your waf, it may not be an executable PHP file."})
            #print(result)
            #resQ.send(result)
    else:
        print("waf is NULL")
        continue