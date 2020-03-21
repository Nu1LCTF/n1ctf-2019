# -*- coding: utf-8 -*-
from core.messq import *
import pymysql
import pymysql.cursors

connect = pymysql.Connect(
    host='cd-cdb-kc73wmz2.sql.tencentcdb.com',
    port=62865,
    user='root',
    passwd='c127359176d04cb5d3d475d8e96bf03e09bdcb5d608c6d6167b16b089980ec32',
    db='n1ctf',
    charset='utf8'
)
cursor = connect.cursor()

Rabbithost = '10.0.20.11'
Rabbituser = 'n1ctf'
Rabbitpass = 'b5d608c6d61'

def insert(score,team):
    sql = "INSERT INTO rank (`team`, `score`,`change`,`time`) VALUES ( %s, %s ,%s , now());"
    cursor.execute(sql,[team,score,"+"+score])
    connect.commit()
    return 0

def update(score,team,change):
    sql = "UPDATE rank SET `score` = %s ,`change` = %s ,`time` = now() WHERE team = %s;"
    cursor.execute(sql,[score,change,team])
    connect.commit()
    return 0

def check_team_score(score,team):
    sql = "SELECT * from rank where team = %s;"
    cursor.execute(sql,[team])
    res = cursor.fetchall()
    if len(res) == 1:
        if int(res[0][2]) < int(score):
            change = "+"+str(int(score)-int(res[0][2]))
            update(score,team,change)
            return 1 # update
        else:
            return 0
    elif len(res) == 0:
        insert(score,team)
        return 2 # insert
    else:
        return 0 # no action

while True:
    resQ = MessageQ(Rabbithost,Rabbituser,Rabbitpass,'result')
    res = resQ.recv()
    res = json.loads(res)
    if res["team"] != "" and res["score"] != "":
        try:
            check_team_score(res["score"],res["team"])
        except:
            continue

#insert("202","nu1l'a")
#update("10","nu1l")
#print(check_team_score("1","nu1l"))
