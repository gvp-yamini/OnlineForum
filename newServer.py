import socket,threading

from forumAPI import *
MAXSIZE = 1024

class mySocket:     #client for requests from socket
    def __init__(self,sock=None):
        if sock == None:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
        else:
            self.sock = sock

    def bind(self,hpTuple):
        self.sock.bind(hpTuple)

    def listen(self):
        self.sock.listen(5)

    def close(self):
        self.sock.close()

    def sendall(self,msg):
        length = len(msg)
        self.sock.sendall(str(length))
        self.sock.recv(1)
        self.sock.sendall(msg)

    def recv(self,max):
        length = self.sock.recv(max)
        self.sock.sendall('k')
        return self.sock.recv(int(length))

    def getData(self,field,msg):
        self.sendall(msg)
        msg = self.recv(MAXSIZE)
        return msg

def main():
    global user
    s = mySocket()
    s.bind(('localhost',9998))
    s.listen()
    msg = ''
    i = 0
    while True:
        print 'Server: Waiting for Client Request'
        client,addr = s.sock.accept()
        cli = mySocket(client)
        i += 1
        print 'Connected with client:{0} Addr: {1}'.format(i,addr)
        t = threading.Thread(None, target =handleClient, args =(cli,addr,))
        t.start()
    s.close()

def handleClient(cli,addr):
    user = guest
    while True:
        msg = cli.recv(MAXSIZE)
        print 'Received from Client:',addr,'-->',msg
        CMD = deserialize(msg)
        if '' in CMD:
            cli.sendall('Command seems to be incomplete')
        elif CMD[0] == 'exit':
            cli.sendall('exit')
            cli.close()
            break
        elif CMD[0] == 'login':
            if user is guest:
                msg,user = login(CMD)
                cli.sendall(msg)
            else:
                cli.sendall('Already Logged In')
        elif CMD[0]=='register':
            msg,user=register(CMD)
            cli.sendall(msg)
        elif CMD[0]=='logout':
            if user is not guest:
                user = guest
                msg='Logout Succesful'
            else:
                msg='not loggedin'
            cli.sendall(msg)
        elif CMD[0]=='addforum':
            msg=add_forum(CMD,user)
            cli.sendall(msg)
        elif CMD[0]=='postquestion':
            msg=postquestion(CMD,user)
            cli.sendall(msg)
        elif CMD[0]=='postanswer':
            msg= postAnswer1(CMD,user)
            cli.sendall(msg)
        elif CMD[0]=='showanswers':
            msg=showAns(CMD)
            cli.sendall(msg)
        elif CMD[0]=='showforums':
            msg=showAllForums(CMD)
            cli.sendall(msg)
        elif CMD[0]=='showquestions':
            msg=showQues(CMD)
            cli.sendall(msg)
        elif CMD[0]=='showstats':
            msg=showStats(CMD)
            cli.sendall(msg)
        else:
            msg = 'Invalid CMD'
            print msg
            cli.sendall(msg)
    cli.close()


def deserialize(msg):
    if len(msg)==0:
        return []
    return msg.split('/')

def register(cmd):
    try:
        username = cmd[1]
        pwd= cmd[2]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    if username.strip() == '' or pwd == '':
        return 'Registration Failed, Give Non-Empty Username and Password',guest
    success = createUser(username,pwd)
    if success:
        return 'Registration Successful',UserState(username)
    else:
        return 'Registration Failed, Username already exists',guest


def login(cmd):
    try:
        username = cmd[1]
        pwd= cmd[2]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS',guest
    success = validateUser(username,pwd)
    if success:
        return 'Login Successful',UserState(username)
    else:
        return 'Login Failed,Check username/pwd',guest

def showStats(cmd):
    try:
        statOf = cmd[1]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    if statOf == 'all':
        pass

def showAllForums(cmd):
    try:
        catid =int(cmd[1])
        if catid not in range(1,6):
            return 'Give valid Category ID'
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    except ValueError:
        return 'Give valid Category ID'
    forumList = showForums(catid)
    if forumList != []:
        msg = '\n'.join(forumList)
        return msg
    return 'No Forums yet in this Category'

def add_forum(cmd,user):
    try:
        catid = int(cmd[1])
        if catid not in range(1,6):
            return 'Invalid Category'
        forum=cmd[2]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    except ValueError:
        return 'Give valid Category ID'
    return user.add_Forum(catid,forum)

def showQues(cmd):
    user = guest
    try:
        cat = int(cmd[1])
        if cat not in range(1,6):
            return 'Invalid Category'
        frm = cmd[2]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    except ValueError:
        return 'Give valid Category ID'
    try:
        next = int(cmd[3])
    except IndexError:
        next = 0
    except ValueError:
        return 'Give valid page number'
    questions = showQuestions(cat,frm,next)
    if questions is False or questions==[]:
        return 'No Questions to display(in this range)'
    msg = []
    for ques in questions:
        msg.append(str(ques[0])+') '+ques[1])
    return '\n'.join(msg)

def showAns(cmd):
    try:
        cat = int(cmd[1])
        if cat not in range(1,6):
            return 'Invalid Category'
        frm = cmd[2]
        qno = int(cmd[3])
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    except ValueError:
        return 'Give valid Question ID or Category Id'
    try:
        next = int(cmd[4])
    except IndexError:
        next = 0
    except ValueError:
        return 'Give valid page number'

    present,response = showAnswers(cat,frm,qno,next)
    if present:
        msg = []
        for ans in response:
            msg.append(str(ans[0])+') '+ans[1])
        return '\n'.join(msg)
    else:
        return response

def postquestion(cmd,user):
    try:
        catId = int(cmd[1])
        if catId not in range(1,6):
            return 'Invalid Category'
        forum = cmd[2]
        qname = cmd[3]
        tags = cmd[4]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    except ValueError:
        return 'Give valid Question ID or Category Id'
    tags = tuple(tags.split(','))
    if len(tags)<2:
        return '2 tags required'
    return user.add_Question(catId, forum, qname,tags)

def postAnswer1(cmd,user):
    try:
        catId = int(cmd[1])
        if catId not in range(1,6):
            return 'Invalid Category'
        forum = cmd[2]
        qid = int(cmd[3])
        ans = cmd[4]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    except ValueError:
        return 'Enter valid Question ID or Category ID'
    return user.add_Answer(catId,forum,qid,ans)



"""def display(category):
    try:
        forums="\n".join(forumsDict[category])
        return forums
    except Exception:
        return "No Forums Available in "+category
"""
if __name__ == '__main__':
    main()