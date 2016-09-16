__author__ = 'Abhi'
import threading
from memoryMain import *

forumLock = threading.Lock()


class UserState:
    nextQ = 0
    nextA = 0
    def __init__(self,username='guest'):
        self.username = username
    def login(self,username):
        self.username = username
    def logout(self):
        self.username = 'guest'
    def add_Forum(self,catid,fname):
        try:
            catid = int(catid)
        except ValueError:
            return 'Enter valid Category'
        if self is guest:
            return 'You are not Logged In'
        if len(fname)>=27:
            return 'Forum name exceeds maximum length'
        forumLock.acquire()
        if f.add_forums(str(catid),fname,self.username):
            #time.sleep(5)
            #forumLock.release()
            forumLock.release()
            return "\n\n\n\n\n\t\tSuccess: Forum Successfully Added"
        forumLock.release()
        return '\n\n\n\n\n\t\t\tNOTE:FAILURE:Forum Already Exists!!!!'

    def add_Question(self,catid,fname,qname,tags):
        if self is guest:
            return 'You are not Logged In'
        if qname.strip()=='':
            return 'Enter valid question'
        if int(catid) in range(1,6):
            forumLock.acquire()
            forums = f.get_forums(catid)
            forumLock.release()
            #print forums
            if fname in forums:
                forumLock.acquire()
                qid = f.add_quesns(catid,fname,qname,self.username,tags)
                forumLock.release()
                return 'Posted Question with id:'+str(qid)
            else:
                #forumLock.release()
                return 'Invalid Forum'
        else:
            return 'Invalid Category'

    def add_Answer(self,catId,fname,qid,answer):
        if self.username is guest:
            return 'You are not Logged In'
        if answer.strip()=='':
            return 'Enter valid Answer'
        if catId in range(1,6):
            forumLock.acquire()
            forums  = f.get_forums(catId)
            forumLock.release()
            if fname in forums:
                #forumLock.acquire()
                questions = getQuestionIDs(catId,fname)
                #forumLock.release()
                if qid in questions:
                    forumLock.acquire()
                    x=str(f.add_answer(catId,fname,qid,answer,self.username))
                    forumLock.release()
                    return 'Posted Answer with id:'+x
                else:
                    return 'Invalid Question'
            else:
                return 'Invalid Forum'
        else:
                return 'Invalid Category'

'''def show_Questions(self,catId, frm,nex):
    if nex==0:
        self.nextQ = 0
    else:
        self.nextQ += nex
    return f.showQuestions(catId,frm,self.nextQ)'''

guest = UserState('guest')

def show_Answers(self,catId, frm,qid,nex = 0):
        if nex==0:
            self.nextA = 0
        else:
            self.nextA += nex
        #forumLock.acquire()
        x=showAnswers(catId,frm,qid,self.nextA)
        #forumLock.release()
        return x

def get_cat():
    return ['Education','Entertainment','Politics','Sports','Other']

def createUser(unm,pwd):
    forumLock.acquire()
    success = r.insert(unm,pwd)
    forumLock.release()
    return success

def validateUser(unm,pwd):
    forumLock.acquire()
    x=r.validate(unm,pwd)
    forumLock.release()
    return x


def showForums(catid):
    try:
        int(catid)
    except ValueError:
        return False,'Enter valid Category ID'
    forumLock.acquire()
    x= f.get_forums(catid)
    forumLock.release()
    return x
def showQuestions(cat,frm,nxt):
    forumLock.acquire()
    x=f.get_quesns(cat,frm,nxt)
    forumLock.release()
    return x


def showAnswers(catId,fname,qid,nxt):
    try:
        int(catId)
    except ValueError:
        return False,'Enter valid Category ID'
    if int(catId) in range(1,6):
        forumLock.acquire()
        AllForums  = f.get_forums(catId)
        forumLock.release()
        if fname in AllForums:
            #forumLock.acquire()
            x=getQuestionIDs(catId,fname)
            #forumLock.release()
            if qid in x:
                forumLock.acquire()
                ans =f.get_answer(catId,fname,qid,nxt)
                forumLock.release()
                if ans == []:
                    return False,'No Answers for this question in this range'
                else:
                    return True,ans
            else:
                return False,'Invalid Question'
            #forumLock.release()
        else:
            return False,'Invalid Forum'

    else:
            return False,'Invalid Category'

def getQuestionIDs(catId,fname):
    qIDs = []
    forumLock.acquire()
    AllqIDS = q.get_questions(catId,fname)
    forumLock.release()
    if AllqIDS is False:
        return qIDs
    for qtuple in AllqIDS:
        qIDs.append(qtuple[0])
    print qIDs
    return qIDs