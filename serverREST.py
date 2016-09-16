from bottle import route, run, request, response
from forumAPI import *

@route('/login',method='POST')
def hello():
    username = request.POST['username']
    password = request.POST['password']
    success = validateUser(username,password)
    if success:
        response.set_cookie('username',username,secret=None,max_age=100,path='/')
        return categories(username)
        #return 'Login Successful'
    else:
        return 'Login Failed,Check username/pwd'
    #return "<html><body>hello client:<a href='/who'> Click here</a></body></html>"

@route('/register',method='POST')
def register():
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return 'INSUFFICIENT ARGUMENTS'
    if username.strip() == '' or password == '':
        return 'Registration Failed, Give Non-Empty Username and Password'
    success = createUser(username,password)
    if success:
        response.set_cookie('username',username,secret=None,max_age=100,path='/')
        return categories(username)
    else:
        return 'Registration Failed, Username already exists'


@route('/logout')
def logout():
    response.delete_cookie('username')
    return 'You are succesfully Logged out. Now you can close'

@route('/who')
def who():
    return 'hai ',request.COOKIES['username']

@route('/categories')
def categories(username="not logged in"):
    msg = '''<p>TEAM 12 FORUMS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;'''+username
    if username != "not logged in":
        msg +='&nbsp;||&nbsp;<a href="/logout">Logout</a></p>'
    msg += '<h2>Categories:</h2><br/>'
    for cat in getCategory.keys():
        msg += '<a href="http://localhost:8081/forums/'+str(cat)+'">'+getCategory[cat]+'</a><br/>'
    return msg

@route('/forums/<catid>')
def showAllForums(catid):
    formForum = "<br/>---------------------------------------------<br/>Create New Forum:<form action='http://localhost:8081/addforum/"+str(catid)+"""' method = 'POST'>
Forum Name:
<input type='text' name='forumname'/>
<button type="submit" name="AddForum">Create Forum</button>
</form>
    """
    try:
        msg = '''<p>TEAM 12 FORUMS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;'''+request.COOKIES["username"]+'&nbsp;||&nbsp;<a href="/logout">Logout</a></p>'
    except KeyError:
        msg = '''<p>TEAM 12 FORUMS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;not loggedin</p>'''
    try:
        catid = int(catid)
        if catid not in range(1,6):
            raise ValueError
        msg += '<h2>Forums in category '+getCategory[catid]+' are:</h2><br/>'
    except ValueError:
        return 'Invalid Category'
    forumList = showForums(catid)
    links =[]
    for eachForum in forumList:
        links.append('<a href="http://localhost:8081/questions/'+str(catid)+'/'+eachForum+'">'+eachForum+'</a>')
    print forumList
    print links
    if forumList != []:
        msg += '<br/>'.join(links)
        return msg+formForum
    return 'No Forums yet in this Category'+formForum

getCategory = {1:'Education',2:'Entertainment',3:'Politics',4:'Sports',5:'Others'}
@route('/questions/<cat>/<frm>')
def showQuestionsDefault(cat,frm):
    return showQues(cat,frm,0)

@route('/questions/<cat>/<frm>/<next>')
def showQues(cat,frm,next):
    formQues = "<br/>---------------------------------------------<br/><form action='/postquestion/"+str(cat)+"/"+frm+"""
    ' method = 'POST'>
Type your Question:
<input type='text' name='question'/>
Tag1:
<input type='text' name='tag1'/>
Tag2:
<input type='text' name='tag2'/>
<br/>
<button type="submit" name="AddQues">Post Question</button>
</form>
    """
    try:
        msg = ['''<p>TEAM 12 FORUMS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;'''+request.COOKIES["username"]+'&nbsp;||&nbsp;<a href="/logout">Logout</a></p>']
    except KeyError:
        msg = ['''<p>TEAM 12 FORUMS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;not loggedin</p>''']
    try:
        cat = int(cat)
        if cat not in range(1,6):
            raise ValueError
    except ValueError:
        return 'Give valid Category ID'
    try:
        next = int(next)
    except ValueError:
        return 'Give valid page number'
    msg.append('<h2>Questions in '+getCategory[cat]+' : '+frm+' are :</h2><br/>')
    questions = showQuestions(cat,frm,next)
    if questions == False:
        msg.append('No Questions to display(in this range)')
    else:
        for ques in questions:
            msg.append('<a href="http://localhost:8081/answers/'+str(cat)+'/'+frm+'/'+str(ques[0])+'">'+str(ques[0])+') '+ques[1]+'</a>')
    return '<br/>'.join(msg)+formQues

@route('/answers/<cat>/<frm>/<qno>')
def showAnswersDefault(cat,frm,qno):
    return showAns(cat,frm,qno,0)

@route('/answers/<cat>/<frm>/<qno>/<next>')
def showAns(cat,frm,qno,next):
    formAns ="<br/>---------------------------------------------<br/><form action='/postanswer/"+str(cat)+"/"+frm+"/"+qno+"""
    ' method = 'POST'>
Type your Answer:
<input type='text' name='answer'/>
<br/>
<button type="submit" name="AddAns">Post Answer</button>
</form>
    """
    try:
        msg = ['''<p>TEAM 12 FORUMS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;'''+request.COOKIES["username"]+'&nbsp;||&nbsp;<a href="/logout">Logout</a></p>']
    except KeyError:
        msg = ['''<p>TEAM 12 FORUMS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;not loggedin</p>''']
    try:
        cat = int(cat)
        if cat not in range(1,6):
            raise ValueError
        qno =int(qno)
    except ValueError:
        return 'Give valid Category ID or Question ID'
    try:
        next = int(next)
    except ValueError:
        return 'Give valid page number'
    msg.append('<h2>Answers in '+getCategory[cat]+' : '+frm+':'+str(qno)+' are :</h2><br/>')
    present,response = showAnswers(cat,frm,qno,next)
    if present:
        for ans in response:
            msg.append(str(ans[0])+') '+ans[1])
        return '<br/>'.join(msg)+formAns
    else:
        msg.append(response)
        return '<br/>'.join(msg)+formAns

@route('/addforum/<catid>',method='POST')
def add_forum(catid):
    try:
        user = request.COOKIES['username']
    except KeyError:
        return 'Please login first'
    try:
        catid = int(catid)
        if catid not in range(1,6):
            raise ValueError
        fname = request.POST['forumname']
    except ValueError:
        return 'Invalid Category'
    except KeyError:
        return 'Please enter forum name'
    return UserState(user).add_Forum(catid,fname)

@route('/postquestion/<catid>/<fname>',method='POST')
def postQuestion(catid,fname):
    try:
        user = request.COOKIES['username']
    except KeyError:
        return 'Please login first'
    try:
        cat = int(catid)
        if cat not in range(1,6):
            raise ValueError
    except ValueError:
        return 'Give valid Category ID'
    try:
        qname = request.POST['question']
    except KeyError:
        return 'Please enter question'
    tags = []
    try:
        tags.append(request.POST['tag1'])
        tags.append(request.POST['tag2'])
    except KeyError:
        return '2 tags required'
    return UserState(user).add_Question(catid, fname, qname,tags)

@route('/postanswer/<catid>/<fname>/<qid>',method='POST')
def postAnswer(catid,fname,qid):
    try:
        user = request.COOKIES['username']
    except KeyError:
        return 'Please login first'
    try:
        catid = int(catid)
        qid = int(qid)
        if catid not in range(1,6):
            raise ValueError
    except ValueError:
        return 'Give valid Category ID and Question ID'
    try:
        ans = request.POST['answer']
    except KeyError:
        return 'Please enter answer'
    return UserState(user).add_Answer(catid,fname,qid,ans)



'''
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
        catid =cmd[1]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    forumList = showForums(catid)
    if forumList != []:
        msg = '\n'.join(forumList)
        return msg
    return 'No Forums yet in this Category'

def add_forum(cmd,user):
    try:
        catid = cmd[1]
        forum=cmd[2]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    return user.add_Forum(catid,forum)

def showQues(cmd):
    user = guest
    try:
        cat = int(cmd[1])
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
    if questions is False:
        return 'No Questions to display(in this range)'
    msg = []
    for ques in questions:
        msg.append(str(ques[0])+') '+ques[1])
    return '\n'.join(msg)

def showAns(cmd):
    try:
        cat = cmd[1]
        frm = cmd[2]
        qno = int(cmd[3])
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    except ValueError:
        return 'Give valid Question ID'
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
        catId = cmd[1]
        forum = cmd[2]
        qname = cmd[3]
        tags = cmd[4]
    except IndexError:
        return 'INSUFFICIENT ARGUMENTS'
    tags = tuple(tags.split(','))
    if len(tags)<2:
        return '2 tags required'
    return user.add_Question(catId, forum, qname,tags)

def postAnswer1(cmd,user):
    try:
        catId = int(cmd[1])
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
'''

run(host='localhost', port=8081, debug=True, reloader=True)
print 'done'