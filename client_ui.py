__author__ = 'Abhi'
import socket
import time
import os
import time
import colorsys
from ctypes import *
import sys
import string
cat_names = ["EDUCATION","ENTERTAINMENT","POLITICS","SPORTS","OTHERS"]
class mySocket:
    def __init__(self,sock=None):
        if sock == None:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
        else:
            self.sock = sock
    def connect(self,hpTuple):
        self.sock.connect(hpTuple)
    def sendall(self,msg):
        length = len(msg)
        self.sock.sendall(str(length))
        self.sock.recv(1)
        self.sock.sendall(msg)
    def recv(self,max):
        length = self.sock.recv(max)
        self.sock.sendall('k')
        return self.sock.recv(int(length))
def main():
    MAXSIZE = 1024
    c = mySocket()
    c.connect(('10.3.9.167',9998))
    def showforums(cmd,cat):
        msg=cmd+'/'+cat
        c.sendall(msg)
        recvbuff=c.recv(MAXSIZE)
        print "\tTHE FORUMS IN THE FOLLOWING",cat
        print "\t--- ------ -- --- ---------  ------------"
        print recvbuff

    def showquestions(cmd,cat,forum):
        msg=cmd+'/'+cat+'/'+forum
        print "\nSending "+cmd+" message:"+msg
        c.sendall(msg)
        recvbuff=c.recv(MAXSIZE)
        print recvbuff

    recvbuff = ''
    while recvbuff != 'exit':
        color1(11,12)
        print "\t\t    -----------------------------------------"
        print "\t\t   | *** WELCOME TO TEAM12 FORUMS WEBSITE *** |"
        print "\t\t    -----------------------------------------"
        print "\n\n"
        print " -------- \t\t ------- \t\t -------- \t\t ------ "
        print "|REGISTER|\t\t| LOGIN |\t\t|  GUEST |\t\t| EXIT |"
        print " -------- \t\t ------- \t\t -------- \t\t ------"
        color1(11,12)
        cmd=raw_input('\n\nFOR FURTHER PROGRESS SELECT ANY OPTION (Enter Help for any doubts) : ')
        if cmd == "help":
            help()
            s = raw_input("\n\n\t\tEnter Some thing to go Back to Menu Page>>")
            if s:
             os.system("cls")
            continue
        if cmd=='login' or cmd=='register':
            while 1:
                    os.system("cls")
                    if cmd == 'register':
                        color1(11,12)
                        print "\n\t\t*** REGISTER PAGE ***"
                        color1(7,8)
                        print "\n\t\t    -------- ----"
                        color1(11,12)
                    else:
                        color1(11,12)
                        print "\n\t\t*** LOGIN PAGE ***"
                        color1(7,8)
                        print "\n\t\t    ----- ----"
                        color1(11,12)

                    username=raw_input("\n\n\t\tENTER USERNAME (Hint:sush/bhagi):")
                    print ("\t\t----- --------")
                    password=raw_input("\t\tENTER PASSWORD (3-4 charectors):")
                    print ("\t\t----- --------")
                    os.system("cls")
                    print "\t\t\tVERIFY"
                    print "\t\t\t------"
                    print "\n\n\n\tUSERNAME : ",username+"\n\n\tPASSWORD : ",password
                    color1(12,13)
                    vary = raw_input("\n\n\tANY CHANGES(HINT:yes or no) : ")
                    vary = string.lower(vary)
                    if vary == "no":
                        color1(7,8)
                        break
                    elif vary == "yes":
                        color1(7,8)
                        continue
            msg=cmd+'/'+username+'/'+password
            c.sendall(msg)
            recvbuff=c.recv(MAXSIZE)
            os.system("cls")
            if recvbuff == "Registration Successful" or recvbuff=="Login Successful":
                color1(10,11)
                print "\n\n\n\n\n\t\t\t"+"****"+recvbuff+"****"
                time.sleep(1)
                os.system("cls")
                color1(7,8)
            else:
                color1(12,13)
                print "\n\n\n\n\n\t\t\t"+"NOTE:"+recvbuff
                time.sleep(1)
                os.system("cls")
                color1(7,8)
                continue
            if(recvbuff=="Registration Successful" or recvbuff=="Login Successful" ):

                while recvbuff=="Login Successful" or recvbuff=="Registration Successful":
                    color1(11,12)
                    print "\n\t\t***  CATEGORIES ***\t\t\t\t\t|LOGOUT|"
                    color1(7,8)
                    print "\t\t     ----------"

                    print "\n\t\t1)EDUCATION\n\n\t\t2)ENTERTAINMENT\n\n\t\t3)POLITICS\n\n\t\t4)SPORTS\n\n\t\t5)OTHERS"
                    cat=raw_input("\n\nCHOOSE CATEGORY ID(HINT(Enter):1/2/3/4/5) :")
                    if cat == "logout":
                         ans = raw_input("Do You Really Want To Exit???")
                         ans = str.lower(ans)
                         if ans == "yes":
                             c.sendall(cmd)
                             os.system("cls")
                             color1(12,13)
                             msg = c.recv(MAXSIZE)
                             print "\n\n\n\n\n\t\t"+msg
                             time.sleep(1)
                             c.sock.close()
                             exit(-1)
                         else:
                             os.system("cls")
                             continue
                    while True:
                        os.system("cls")
                        color1(11,12)
                        print "\t      \t             \t\t\t\t\t|LOGOUT|\n\n"
                        print "\n\n\t1)ADDFORUMS (cmd:addforum)\n\t2)SHOWFORUMS (cmd:showforums)\n\t3)PREVIOUS PAGE (cmd:previouspage)\n"
                        color1(11,12)
                        cmd=raw_input("\n\nENTER OPTION ->")
                        os.system("cls")
                        if cmd == "previouspage":
                            color1(11,12)
                            break
                        if cmd=="addforum":
                            os.system("cls")
                            color1(11,12)
                            print "\n\n\t\tADD FORUM PAGE"
                            color1(7,8)
                            print "\t\t--- ----- ----"
                            forumname=raw_input("\n\n\t\tENTER FORUM NAME : ")
                            msg1=cmd+'/'+cat+'/'+forumname
                            c.sendall(msg1)
                            recvbuff1=c.recv(MAXSIZE)
                            if recvbuff1 == "\n\n\n\n\n\t\tSuccess: Forum Successfully Added":
                                color1(10,11)
                                print "\t"+recvbuff1
                                time.sleep(2)
                            else:
                                os.system("cls")
                                color1(12,13)
                                if recvbuff == "\n\n\n\n\n\t\tNOTE:FAILURE:Forum Already Exists!!!!":
                                    print recvbuff
                                    color1(11,12)
                                else:
                                    print "\n\n\n\n\n\t\t\t"+"NOTE:"+recvbuff1
                                    time.sleep(2)
                                    color1(11,12)
                        elif cmd=="showforums":
                            msg1 = cmd+'/'+cat
                            c.sendall(msg1)
                            recvbuff = c.recv(MAXSIZE)
                            print "\t\t\tFORUMS IN",cat_names[int(cat)-1]+"\n\n"
                            if recvbuff == "No Forums yet in this Category" or recvbuff== "INSUFFICIENT ARGUMENTS":
                                color1(12,13)
                                print "\n\n\n\n\n\t\t"+recvbuff
                                time.sleep(2)
                                os.system("cls")
                                color1(11,12)
                                continue
                            else:
                                recvbuff = recvbuff.split('\n')
                                i = 0
                                s1=''
                                l=len(recvbuff)
                                for i in range(l):
                                     s1+="%20s"%recvbuff[i]
                                     if i%4==3:
                                      s1+='\n'
                                     print s1

                            forum=raw_input("\n\n\t\t SELECT A FORUM : ")
                            while True:
                                os.system("cls")
                                s = string.lower(forum)
                                print "\n\n\t\t\t",str.upper(s) + "PAGE\n\n"
                                print "\t\t\t\t\t\tLOGOUT\n\n\t\t1)POST QUESTION (hint:cmd:postquestion)\n\n\t\t2)SHOW QUESTIONS (hint:cmd:showquestions\n\n\t\t3)PREVIOUSPAGE (hint:cmd:previouspage)"
                                cmd=raw_input("\n\n\t\tENTER YOUR CHOICE:")
                                print "\t\t----- ---- ------"
                                if cmd=="postquestion" or cmd == "postanswer" or cmd == cmd=="showquestions" or cmd =="showanswers":
                                  if cmd == "postquestion":
                                    question=raw_input("\n\nENTER QUESTION:")
                                    tags=raw_input("\n\nENTER TAGS(Hint:Compulsory 2 tags separated by{','}:")
                                    msg1=cmd+'/'+cat+'/'+forum+'/'+question+'/'+tags
                                    c.sendall(msg1)
                                    recvbuff1=c.recv(MAXSIZE)
                                    if recvbuff == "INSUFFICIENT ARGUMENTS" or recvbuff=='2 tags required':
                                     print "\n\n\n\n\n\t\t\t"+recvbuff1
                                     time.sleep(2)
                                     os.system("cls")
                                     color1(11,12)
                                    else:
                                        os.system("cls")
                                        color1(10,11)
                                        print "\n\n\n\n\n\t\t\t"+recvbuff1
                                        time.sleep(2)
                                        color1(11,12)
                                    continue
                                  elif cmd=="showquestions":
                                        count = 0
                                        msg = cmd+'/'+cat+'/'+forum
                                        c.sendall(msg)
                                        recvbuff = c.recv(MAXSIZE)
                                        os.system("cls")
                                        print "\n\n\t\t\t\t",str.upper(forum)+' '+"PAGE"
                                        if recvbuff == 'INSUFFICIENT ARGUMENTS'or recvbuff=='Give valid page number' or recvbuff=='Give valid Category ID'or recvbuff=='No Questions to display(in this range)':
                                            os.system("cls")
                                            color1(11,12)
                                            print "\n\n\n\n\n\t\t\t"+recvbuff
                                            time.sleep(1)
                                            color1(11,12)
                                            continue
                                        else:
                                            print recvbuff
                                        while True:
                                         ans = raw_input("\n\nDO YOU WANT TO VIEW MORE QUESTIONS(yes or no)????")
                                         if str.lower(ans) == "yes":
                                            count += 1
                                            msg = cmd+'/'+cat+'/'+forum+'/'+count
                                            c.sendall(msg)
                                            recvbuff = c.recv(MAXSIZE)
                                            print recvbuff
                                            if recvbuff == 'No Questions to display(in this range)':
                                                color1(12,13)
                                                print recvbuff
                                                time.sleep(1)
                                                color1(11,12)
                                                break

                                            continue
                                         else:
                                             color1(11,12)
                                             break
                                        print "\n\n\t\tSHOW ANSWERS(cmd:showanswers)\tPOST ANSWERS(cmd:postanswer)"
                                        if cmd =="showanswers" or cmd == "postanswer":
                                         opt = raw_input("\n\n\tEnter Option>>")

                                         ques = raw_input("\n\nENTER QUESTION ID")
                                         msg = cmd+'/'+cat+'/'+forum+'/'+ques
                                         c.sendall(msg)
                                         recvbuff = c.recv(MAXSIZE)
                                         if cmd == "showanswers":
                                               if recvbuff == recvbuff == 'INSUFFICIENT ARGUMENTS' or recvbuff=='Give valid Question ID or Category Id'or recvbuff=='No Answer yet for this Question'or recvbuff=='Invalid Question'or recvbuff=='Invalid Forum' or recvbuff=="Invalid Category":
                                                   os.system("cls")
                                                   time.sleep(1)
                                                   color1(12,13)
                                                   print "\n\n\n\n\n\t\t\t"+"NOTE:"+recvbuff
                                                   time.sleep(2)
                                                   os.system("cls")
                                                   color1(11,12)
                                                   continue
                                               else:
                                                   os.system("cls")
                                                   color1(10,11)
                                                   print "\n\n\t\tTHE ANSWER FOR THE FOLLOWING QUESTION ID :",ques
                                                   print "\n\n"+recvbuff
                                                   time.sleep(2)
                                                   color1(11,12)
                                                   break
                                         elif cmd == "postanswer":
                                           os.system("cls")
                                           if recvbuff == "Invalid Forum" or recvbuff == "Invalid Category" or recvbuff == "Invalid Question" or recvbuff=='Enter valid Question ID or Category ID':
                                            color1(12,13)
                                            print "\n\n\n\n\n\t\t\t"+"NOTE:"+recvbuff
                                            color1(11,12)
                                            continue
                                           else:
                                               os.system("cls")
                                               color1(11,12)
                                               print "\n\n\n\n\n\t\t"+recvbuff
                                               os.system("cls")
                                               break

                                        else:
                                            os.system("cls")
                                            color1(12,13)
                                            print "INVALID OPTION"
                                            color1(11,12)
                                            continue
                                elif cmd=="previouspage":
                                    os.system("cls")
                                    color1(11,12)
                                    break
                                elif cmd == "logout":
                                     ans = raw_input("Do You Really Want To Exit???")
                                     ans = str.lower(ans)
                                     if ans == "yes":
                                         c.sendall(cmd)
                                         os.system("cls")
                                         color1(12,13)
                                         msg = c.recv(MAXSIZE)
                                         print "\n\n\n\n\n\t\t"+msg
                                         time.sleep(1)
                                         c.sock.close()
                                         exit(-1)
                                     else:
                                         os.system("cls")
                                         color1(11,12)
                                         continue
                                else:
                                    os.system("cls")
                                    color1(12,13)
                                    print "\n\n\n\n\n\t\t\tINVALID OPTION"
                                    print "\t\t\t------- ------"
                                    time.sleep(1)
                                    color1(11,12)
                                    continue
                        elif cmd=="logout":
                                     ans = raw_input("Do You Really Want To Exit???")
                                     ans = str.lower(ans)
                                     if ans == "yes":
                                         c.sendall(cmd)
                                         os.system("cls")
                                         color1(12,13)
                                         msg = c.recv(MAXSIZE)
                                         print "\n\n\n\n\n\t\t"+msg
                                         time.sleep(1)
                                         c.sock.close()
                                         exit(-1)
                                     else:
                                         os.system("cls")
                                         color1(11,12)
                                         continue
                else:
                            os.system("cls")
                            color1(12,13)
                            print "\n\n\n\n\n\t\t\tINVALID OPTION"
                            time.sleep(1)
                            os.system("cls")
                            color1(11,12)
                            continue
            else:
                color1(11,12)
                break

        elif cmd=="guest":
                color1(12,13)
                print "\n\n\tNOTE : UNREGISTERED USERS CAN ONLY USE SHOW OPTIONS"
                print "\t----   ------------ ----- --- ---- --- ---- -------"
                print "\n\t\t***  CATEGORIES ***\t\t\t  EXIT"
                print "  \t\t-------------------"
                print "\n\t\t1)EDUCATION\n\t\t2)ENTERTAINMENT\n\t\t3)POLITICS\n\t\t4)SPORTS\n\t\t5)OTHERS"
                cat=raw_input("\n\nCHOOSE CATEGORY ID(HINT:1/2/3/4/5) :")
                os.system("cls")
                while True:
                    print "\n\n\t\tGUEST USERS FORUM PAGE"
                    print "\t\t----- ----- ----- ----"
                    print "\n\t\t1)SHOW FORUMS(cmd:showforums)\n\t\t2)PREVIOUS PAGE(cmd:previouspage)"
                    cmd=raw_input("\n\nENTER OPTION->")
                    if cmd=="showforums":
                        showforums(cmd,cat)
                        forum=raw_input("\n\n\tENTER A FORUM : ")
                        os.system("cls")
                        print "\n\n\t\t\t\t",str.upper(forum)+' '+"PAGE"
                        print "\n\t1)SHOW QUESTIONS(cmd:showquestions)\n\t2)SHOW ANSWERS(cmd:showanswers)\n\t3)PREVIOUS PAGE(cmd:previouspage)\n\t4)EXIT"
                        cmd = raw_input("ENTER OPTION : >>")
                        if cmd == "previouspage":
                            color1(11,12)
                            break
                        if cmd=="showquestions" or cmd =="showanswers":
                                        count = 0
                                        msg = cmd+'/'+cat+'/'+forum
                                        c.sendall(msg)
                                        recvbuff = c.recv(MAXSIZE)
                                        os.system("cls")
                                        print "\n\n\t\t\t\t",str.upper(forum)+' '+"PAGE"

                                        if recvbuff == 'INSUFFICIENT ARGUMENTS'or recvbuff=='Give valid page number' or recvbuff=='Give valid Category ID'or recvbuff=='No Questions to display(in this range)':
                                            os.system("cls")
                                            color1(12,13)
                                            print "\n\n\n\n\n\t\t"+recvbuff
                                            color1(11,12)
                                            continue
                                        else:
                                            print recvbuff
                                        while True:
                                         ans = raw_input("\n\nDO YOU WANT TO VIEW MORE QUESTIONS(yes or no)????")
                                         if str.lower(ans) == "yes":
                                            count += 1
                                            msg = cmd+'/'+cat+'/'+forum+'/'+count
                                            c.sendall(msg)
                                            recvbuff = c.recv(MAXSIZE)
                                            print recvbuff
                                            if recvbuff == '\t\tNO QUESTIONS TO BE DISPLAYED IN THIS FORUM\t\t':
                                                color1(11,12)
                                                break
                                            color1(11,12)
                                            continue
                                         else:
                                             color1(11,12)
                                             break
                                         print "\n\n\t\tSHOW ANSWERS(cmd:showanswers)\tADD ANSWERS(cmd:addanswer)"
                        if cmd =="showanswers":
                              ques = raw_input("\n\nENTER QUESTION ID")
                              msg = cmd+'/'+cat+'/'+forum+'/'+ques
                              c.sendall(msg)
                              recvbuff = c.recv(MAXSIZE)
                              os.system("cls")
                              print "\n\n\t\tTHE ANSWER FOR THE FOLLOWING QUESTION ID :",ques
                              print "\n\n"+recvbuff
                        else:
                                color1(11,12)
                                break
                        if cmd == "exit":
                              ans = raw_input("Do You Really Want To Exit???")
                              ans = str.lower(ans)
                              if ans == "yes":
                                     c.sendall(cmd)
                                     os.system("cls")
                                     color1(12,13)
                                     print "\n\n\n\n\t\t\tExiting Out From Forums!!!"
                                     time.sleep(1)
                                     c.sock.close()
                                     exit(-1)
                              else:
                                    color1(11,12)
                                    continue

                    elif cmd=="previouspage":
                        color1(11,12)
                        break
                    elif cmd == "exit":
                        os.system("cls")
                        print "\n\n\n\n\t\t\tLogging Out From Forums!!!"
                        time.sleep(1)
                        c.sendall(cmd)
                        c.sock.close()
                        exit(-1)
                    else:
                        os.system("cls")
                        color1(12,13)
                        print "\n\n\n\n\n\t\tINVALID OPTION"
                        time.sleep(1)
                        color1(11,12)
                        break

        elif cmd=="exit":
            os.system("cls")
            color1(12,13)
            ns = raw_input("\n\n\n\t\tDo You Really Want To Exit???")
            ans = str.lower(ans)
            if ans == "yes":
                 c.sendall(cmd)
                 os.system("cls")
                 recvbuff = c.recv(MAXSIZE)
                 print "\n\n\n\n\n\t\t\t"+recvbuff
                 time.sleep(1)
                 c.sock.close()
                 exit(-1)
            else:
             color1(11,12)
             continue
        else:
            os.system("cls")
            color1(12,13)
            print " NOTE : INVALID OPTION"
            time.sleep(1)
            os.system('cls')
            color1(11,12)
            continue
    c.sock.close()
def help():
    os.system("cls")
    print "\n\n\t\t\tWELCOME TO TEAM12 FORUMS(HELP PAGE)\n\n"
    print "\t\t\t------- -- ------ ------- ----- -----"
    print "\n\t\t\tWe Provide the User the following Features:"
    print "\n\t1.Users Can Login or Register\n\n\t2)Unregistered Users Can access Only Show Options\n\n\t3)We Provide The Following Commands\n\n\ta)ADD FORUMS(cmd:addforum)\n\n\tb)SHOW FORUMS(cmd:showforums/unregistered user can also access)\n\n\tc)POST QUESTION(cmd:addquestion)\n\n\t\d)SHOW QUESTIONS(cmd:showquestions/unregistered user can also access)\n\n\te)POST ANSWER(cmd:postanswer)\n\n\tf)SHOW ANSWERS(cmd:showanswers/unregistered user can also access)\n\n\tg)LOGOUT(cmd:logout)\n\n\th)EXIT(cmd:EXIT)"
def color1(x,y):
    windll.Kernel32.GetStdHandle.restype = c_ulong
    h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
    for color in xrange(x,y):
         windll.Kernel32.SetConsoleTextAttribute(h, color)
if __name__ == '__main__':
    main()
