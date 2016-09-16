__author__ = 'User'
from file_IO import *
import random
import time

class forums:
    def __init__(self):
        self.forum_data=[]
        self.forum_cache=[None]*10
        self.questions=[[],[],[],[],[],[],[],[],[],[]]
        self.l1=[]
        self.answer_cache=['','',1,[]]

    def add_forums(self,cat_name,forum_name,user_name):
        forum=[]
        k=int(cat_name)
        l2=self.forum_data[k-1]
        for i in range(len(l2)):
            forum.append(l2[i].strip())
        if forum_name in forum:
            return False
        x=s.create_forum(cat_name,forum_name,user_name)

        if not x:
            return False
        self.forum_data[k-1].append(forum_name)
        return True

    def get_forums(self,cat_name):
        x=self.forum_data[int(cat_name)-1]
        #for y in x:

            #l1.append(y.strip())
        return x

    def add_quesns(self,c_id,forum_name,question,user_name,tags):
        x=q.create_question(c_id,forum_name,question,user_name,tags)
        if(forum_name in self.forum_cache):
            i=self.forum_cache.index(forum_name)
            self.questions[i].append((x,question))
        return x

    def get_quesns(self,c_id,forum_name,count):
        if(forum_name in self.forum_cache):
            i=self.forum_cache.index(forum_name)
            try:
                return self.questions[i][count*10:count*10+10]
            except Exception:
                return False
        if(None in self.forum_cache ):
            i=self.forum_cache.index(None)
            self.forum_cache[i]=(forum_name,time.asctime())
            self.questions[i]=q.get_questions(c_id,forum_name)
            try:
                 return self.questions[i][count*10:count*10+10]
            except Exception:
                return False
        k='zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
        for i in range(10):
            if(self.forum_cache[i][1]<k):
                k=self.forum_cache[i][1]
                l=i
        self.forum_cache[l]=(forum_name,time.asctime())
        self.questions[l]=q.get_questions(c_id,forum_name)
        try:
            return self.questions[l][count*10:count*10+10]
        except Exception:
            return False


    def add_answer(self,cat_id,forum_name,q_id,answer,username):
        if(self.answer_cache[0]==cat_id and self.answer_cache[1]==forum_name and self.answer_cache[2]==q_id):
            self.answer_cache[3].append(answer)
        self.answer_cache[0]=cat_id
        self.answer_cache[1]=forum_name
        self.answer_cache[2]=q_id
        id= a.create_answer(cat_id,forum_name,q_id,answer,username)
        self.answer_cache[3]=a.get_answers(cat_id,forum_name,q_id)
        return id

    def get_answer(self,cat_id,forum_name,q_id,count):

        if(self.answer_cache[0]==cat_id):
            if(self.answer_cache[1]==forum_name):
                if(self.answer_cache[2]==q_id and count==0):
                    return self.answer_cache[3][count*10:count*10+10]
        x= a.get_answers(cat_id,forum_name,q_id)
        if x==False:
            return False
        self.answer_cache[0]=cat_id
        self.answer_cache[1]=forum_name
        self.answer_cache[2]=q_id
        self.answer_cache[3]=x


        return self.answer_cache[3][count*10:count*10+10]


f=forums()

for i in range(1,6):
    f.forum_data.append(s.get_forums(str(i)))
#print f.get_quesns('1','bondy',3)
#print f.get_quesns('1','xy98',0)
#f.add_answer("1","threads",3,"this is thread","bondy")
#print f.get_answer('1','threads',3,0)
#for x in f.forum_data:
#    for y in x:
#        print y
"""f.get_forums('1')
x = f.get_quesns('2','Algorithms99',0)

for y in x:
    print y
#f.get_answer('2','Algorithms99','200000',0,"bondy")
#f.add_answer('3','OperatingSys99',20000,'who s this?','a')
x= f.get_quesns('1','cs0',1)
for y in x:
    print y
 def get_questions(self,forum_name,cat_name):
        if(forum_name not in self.forum_cache):
            for i in range(len(self.forum_cache)):
                if(self.forum_cache[i]==[]):
                    self.forum_cache[i].append(forum_name)
                    break
        i=self.forum_cache.index(forum_name)
        self.questions[i]=f1.get_forums(forum_name,cat_name)
"""

"""s="dict"
for i in range(10):
    x=s+str(i)
    f.add_forums("Education",x,"bondy")"""