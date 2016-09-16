__author__ = 'Ravi'
import struct
import time



import struct
class Begin:
    def __init__(self):
        try:
            self.fp=open("forums.bin","rb+")
            self.fp.seek(4*0)
            x=self.fp.read(4)
            self.users_offset=struct.unpack("I",x)
            self.fp.seek(4*1)
            self.no_of_users=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*2)
            self.forum_offset=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*3)
            self.ques_offset=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*4)
            self.act_ques_pointer=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*5)
            self.no_of_ques=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*6)
            self.ans_offset=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*7)
            self.act_ans_pointer=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*8)
            self.no_of_ans=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*9)
            self.rep_offset=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*10)
            self.act_reply_pointer=struct.unpack("I",self.fp.read(4))
            self.fp.seek(4*11)
            self.no_of_rep=struct.unpack("I",self.fp.read(4))
            self.fp.close()
        except IOError:
            self.fp=open("forums.bin","wb+")
            self.fp.seek(1024*1024*1024-3)
            self.fp.write("End")
            self.users_offset=1024
            self.no_of_users=0
            self.forum_offset=1024*1024
            self.ques_offset=3*1024*1024
            self.act_ques_pointer=123*1024*1024
            self.no_of_ques=1
            self.ans_offset=33*1024*1024
            self.act_ans_pointer=323*1024*1024
            self.no_of_ans=1
            self.rep_offset=103*1024*1024
            self.act_reply_pointer=883*1024*1024
            self.no_of_rep=1
            self.fp.seek(0)
            x=struct.pack("I",1024)
            self.fp.write(x)
            self.fp.seek(4)
            self.fp.write(struct.pack("I",self.no_of_users))
            self.fp.seek(4*2)
            self.fp.write(struct.pack("I",self.forum_offset))
            self.fp.seek(4*3)
            self.fp.write(struct.pack("I",self.ques_offset))
            self.fp.seek(4*4)
            self.fp.write(struct.pack("I",self.act_ques_pointer))
            self.fp.seek(4*5)
            self.fp.write(struct.pack("I",self.no_of_ques))
            self.fp.seek(4*6)
            self.fp.write(struct.pack("I",self.ans_offset))
            self.fp.seek(4*7)
            self.fp.write(struct.pack("I",self.act_ans_pointer))
            self.fp.seek(4*8)
            self.fp.write(struct.pack("I",self.no_of_ans))
            self.fp.seek(4*9)
            self.fp.write(struct.pack("I",self.rep_offset))
            self.fp.seek(4*10)
            self.fp.write(struct.pack("I",self.act_reply_pointer))
            self.fp.seek(4*11)
            self.fp.write(struct.pack("I",self.no_of_rep))
            #self.fp.seek(1024*1024*1024-3)
            #self.fp.write("End")
            self.fp.close()
            c = Category()
            c.create_category()

class Register:
    #Initilizing user metadata.
    def __init__(self):
        b=Begin()
        self.no_of_users=b.no_of_users[0]
        self.start_offset=b.users_offset[0]
        #last_offset=1024
        try:
            self.fp=open("forums.bin","rb+")
        except IOError:
            self.fp=open("forums.bin","wb+")



    #Inserting user details into the file.
    def insert(self,user_name,paswrd):
        if user_name=="" or paswrd=="":
            return False
        i=0
        self.fp.seek(self.start_offset)
        while(i<self.no_of_users):
           self.fp.seek(self.start_offset+i*24)
           if self.fp.read(12).strip()==user_name:
               return False
           i+=1
        self.fp.seek(self.start_offset+i*24)
        self.fp.write(struct.pack("12s12s",user_name.ljust(12),paswrd.ljust(12)))
        self.no_of_users+=1
        self.fp.seek(0)
        self.fp.write(struct.pack("I",self.start_offset))
        self.fp.seek(4)
        self.fp.write(struct.pack("I",self.no_of_users))

        return True


    def validate(self,user_name,paswrd):
        i=0

        while(i<self.no_of_users):
           self.fp.seek(self.start_offset+i*24)
           if self.fp.read(12).strip()==user_name and self.fp.read(12).strip()==paswrd:
               self.fp.seek(self.start_offset+i*24)
               return struct.pack("12s12s",user_name.ljust(12),paswrd.ljust(12))
           i+=1

        return False



class Category:
    def __init__(self):
        self.cat_names={1:"Education",2:"Sports",3:"Poilitics",4:"Entertainment",5:"Others"}
        self.offset=1048416
        try:
            self.fp=open("forums.bin","rb+")
        except IOError:
            self.fp=open("forums.bin","wb+")
    def create_category(self):
        i=1
        self.fp.seek(self.offset,0)
        while i<6:
            self.fp.write(struct.pack("1s15sII8s",str(i),self.cat_names[i].ljust(15),1,1,"".ljust(8)))
            i+=1
        self.fp.close()
        return True

class Forums:
    def __init__(self):
        b=Begin()
        self.offset=b.forum_offset[0]
        try:
            self.fp=open("forums.bin","rb+")
        except IOError:
            self.fp=open("forums.bin","wb+")
    def create_forum(self,c_id,forum_name,user_name):
        i=0
        if forum_name=="":
            return False
        c_id=int(c_id)
        self.fp.seek(1024*1024-((6-c_id)*32))
        s=self.fp.read(32)
        t=struct.unpack("1s15sII8s",s)
        self.fp.seek(1024*1024-((6-c_id)*32))

        if t[3]==1:
            self.fp.write((struct.pack("1s15sII8s",t[0],t[1],self.offset,self.offset,t[4])))
        elif self.offset>=(2*1024*1024):
            return False
        else:
            self.fp.write((struct.pack("1s15sII8s",t[0],t[1],t[2],self.offset,t[4])))

        self.fp.seek(self.offset)
        if t[2]==1:
            meta_data=struct.pack("I1s27s12sII12s",self.offset,str(c_id),forum_name.ljust(27),user_name.ljust(12),1,1,"".ljust(12))
            self.fp.write(meta_data)
        else:
            meta_data=struct.pack("I1s27s12sII12s",t[3],str(c_id),forum_name.ljust(27),user_name.ljust(12),1,1,"".ljust(12))
            self.fp.write(meta_data)
        self.offset+=64
        self.fp.seek(8)
        self.fp.write(struct.pack("I",self.offset))

        #self.fp.close()
        return True



    def get_forums(self,c_id):
        #c_id=int(c_id)
        self.fp.seek(1024*1024-((6-int(c_id))*32))
        s=self.fp.read(32)
        x=struct.unpack("1s15sII8s",s)
        meta_data=[]
        if x[3]!=1:
            self.fp.seek(x[3])
            s=self.fp.read(64)
            t=struct.unpack("I1s27s12sII12s",s)
            meta_data.append(t[2].strip())
            while (t[0]!=1 or len(meta_data)==0) and t[1]==c_id:
                self.fp.seek(t[0])
                s=self.fp.read(64)
                t=struct.unpack("I1s27s12sII12s",s)
                meta_data.append(t[2].strip())
                print self.fp.tell()-64,t[0]
                if t[0]==1 or t[0]==self.fp.tell()-64:
                    break
        else:
            return []
        return meta_data
        '''
        if len(meta_data)==1:
            return meta_data
        #self.fp.seek(1024*1024-((6-c_id)*32))
        else:
            return meta_data[:-1]
        '''


    def close(self):
        self.fp.close()

class Questions:
    def __init__(self):
        b=Begin()
        self.offset=b.ques_offset[0]
        self.act_question_pointer=b.act_ques_pointer[0]
        self.questions=b.no_of_ques[0]
        try:
            self.fp=open("forums.bin","rb+")
        except IOError:
            self.fp=open("forums.bin","wb+")

    def create_question(self,c_id,forum_name,question,user_name,tags):
        #i=0
        c_id=int(c_id)
        self.fp.seek(1024*1024-((6-c_id)*32))
        s=self.fp.read(32)
        t=struct.unpack("1s15sII8s",s)
        if t[2]==1:
            return False
        self.fp.seek(t[3])
        s=self.fp.read(64)
        s=struct.unpack("I1s27s12sII12s",s)
        #print s
        while s[2].strip()!=forum_name and s[0]!=t[2]:
            print "loop"
            self.fp.seek(s[0])
            s=self.fp.read(64)
            s=struct.unpack("I1s27s12sII12s",s)
        if(s[2].strip()!=forum_name and s[0]==1):
            return False
        if s[4]==1 and s[5]==1:
            pointer_first=self.offset
            pointer_last=self.offset
            flag=0
            #self.fp.seek(pointer_first)
        else:
            flag=1
            #self.fp.seek(pointer_first+64)
            pointer_first=self.offset
            pointer_last=s[5]
        #self.fp.write(pointer_first)
        #self.fp.write(pointer_last)
        self.fp.seek(self.fp.tell()-64)
        if flag==0:
            #print self.fp.tell()
            self.fp.write(struct.pack("I1s27s12sII12s",s[0],s[1],s[2],s[3],pointer_first,pointer_last,s[6]))
            self.fp.seek(pointer_first)
        else:
            self.fp.write(struct.pack("I1s27s12sII12s",s[0],s[1],s[2],s[3],pointer_first,s[5],s[6]))
            self.fp.seek(pointer_first+64)

        t=time.asctime()
        if self.questions!=1:
            x=struct.pack("III8s8s12sIIII28sI24s16s",self.questions,1,1,tags[0].ljust(8),tags[1].ljust(8),user_name.ljust(12),1,1,self.act_question_pointer,s[4],forum_name.ljust(28),len(question),t,"".ljust(16))
        else:
            x=struct.pack("III8s8s12sIIII28sI24s16s",self.questions,1,1,tags[0].ljust(8),tags[1].ljust(8),user_name.ljust(12),1,1,self.act_question_pointer,1,forum_name.ljust(28),len(question),t,"".ljust(16))

        self.fp.seek(self.offset)
        self.questions+=1
        self.fp.write(x)
        length=len(question)
        self.fp.seek(self.act_question_pointer)
        self.fp.write(question)
        self.act_question_pointer+=length
        #self.fp.close()
        self.offset+=128
        self.fp.seek(12)
        self.fp.write(struct.pack("I",self.offset))
        self.fp.seek(16)
        self.fp.write(struct.pack("I",self.act_question_pointer))
        self.fp.seek(20)
        self.fp.write(struct.pack("I",self.questions))
        return self.questions-1


    def get_questions(self,c_id,forum_name):
        c_id=int(c_id)
        self.fp.seek(1024*1024-((6-c_id)*32))
        s=self.fp.read(32)
        t=struct.unpack("1s15sII8s",s)
        if t[3]==1:
            return False
        self.fp.seek(t[3])
        s=self.fp.read(64)
        s=struct.unpack("I1s27s12sII12s",s)

        while s[2].strip()!=forum_name and s[0]!=1:
            self.fp.seek(s[0])
            s=self.fp.read(64)
            if len(s)==64:
                s=struct.unpack("I1s27s12sII12s",s)
            else:
                break
            if s[0]==self.fp.tell()-64:
                if self.fp.tell()-128>=3*1024*1024:
                    self.fp.seek(self.fp.tell()-128)
                    s=self.fp.read(64)
                    s=struct.unpack("I1s27s12sII12s",s)
                else:
                    break
        meta_data=[]
        #if s[0]==1:
            #return False

        if s[4]!=1:
            self.fp.seek(s[4])
            s=self.fp.read(128)
            t=struct.unpack("III8s8s12sIIII28sI24s16s",s)
            self.fp.seek(t[8])
            s=self.fp.read(t[11])
            meta_data.append((t[0],s))
            while t[9]!=1 and t[10].strip()==forum_name:
                self.fp.seek(t[9])
                s=self.fp.read(128)
                t=struct.unpack("III8s8s12sIIII28sI24s16s",s)
                self.fp.seek(t[8])
                s=self.fp.read(t[11])
                meta_data.append((t[0],s))
        else:
            return False
        return meta_data
        """
        if t[9]==1:
            return meta_data
        else:
            return meta_data[:-1]
        """
    def close(self):
        self.fp.close()




class Answers:
    def __init__(self):
        b=Begin()
        self.offset=b.ans_offset[0]
        self.act_answer_pointer=b.act_ans_pointer[0]
        self.answers=b.no_of_ans[0]
        try:
            self.fp=open("forums.bin","rb+")
        except IOError:
            self.fp=open("forums.bin","wb+")
    def create_answer(self,c_id,forum_name,ques_id,answer,user_name):
        if self.offset>=103*1024*1024:
            return False
        c_id=int(c_id)
        self.fp.seek(1024*1024-((6-c_id)*32))
        s=self.fp.read(32)
        t=struct.unpack("1s15sII8s",s)
        if t[3]==1:
            return False
        self.fp.seek(t[3])
        s=self.fp.read(64)
        s=struct.unpack("I1s27s12sII12s",s)


        while s[2].strip()!=forum_name and s[0]!=1:
            self.fp.seek(s[0])
            s=self.fp.read(64)
            s=struct.unpack("I1s27s12sII12s",s)
        self.fp.seek(s[4])

        s=self.fp.read(128)
        s=struct.unpack("III8s8s12sIIII28sI24s16s",s)

        while s[0]!=ques_id and s[10].strip()==forum_name:
            self.fp.seek(s[9])
            s=self.fp.read(128)
            s=struct.unpack("III8s8s12sIIII28sI24s16s",s)
        #print s
        if s[0]==1 and s[10].strip()!=forum_name:
                return False
        pointer_first=s[6]
        pointer_last=s[7]
        if pointer_first==1 and pointer_last==1:

            pointer_first=self.offset
            pointer_last=self.offset
        else:
            pointer_last=s[7]
            pointer_first=self.offset

        self.fp.seek(self.fp.tell()-128)
        s=self.fp.read(128)
        m=time.time()
        s=struct.unpack("III8s8s12sIIII28sI24s16s",s)
        self.fp.seek(self.fp.tell()-128)
        j=0

        x=struct.pack("III8s8s12sIIII28sI24s17s",s[0],s[1],s[2],s[3],s[4],s[5],pointer_first,pointer_last,s[8],s[9],s[10],s[11],s[12],s[13])
        self.fp.write(x)
        self.fp.seek(pointer_first)




        t=time.asctime()
        #print ques_id
        if self.offset!=33*1024*1024:
           x=struct.pack("IIIIIII12sI24sI56s",self.answers,0,0,self.act_answer_pointer,s[6],1,1,user_name.ljust(12),len(answer),t,ques_id,"".ljust(56))
        else:
            x=struct.pack("IIIIIII12sI24sI56s",self.answers,0,0,self.act_answer_pointer,self.offset,1,1,user_name.ljust(12),len(answer),t,ques_id,"".ljust(56))
        self.fp.write(x)

        self.answers+=1
        length=len(answer)
        self.fp.seek(self.act_answer_pointer)
        self.fp.write(answer)
        self.act_answer_pointer+=length


        self.offset+=128
        self.fp.seek(24)
        self.fp.write(struct.pack("I",self.offset))
        self.fp.seek(28)
        self.fp.write(struct.pack("I",self.act_answer_pointer))
        self.fp.seek(32)
        self.fp.write(struct.pack("I",self.answers))
        #self.fp.close()

        return self.answers-1



    def get_answers(self,c_id,forum_name,ques_id):
            c_id=int(c_id)
            self.fp.seek(1024*1024-((6-c_id)*32))
            s=self.fp.read(32)
            t=struct.unpack("1s15sII8s",s)
            if t[3]==1:
                return False
            self.fp.seek(t[3])
            s=self.fp.read(64)

            s=struct.unpack("I1s27s12sII12s",s)


            while s[2].strip()!=forum_name and s[0]!=1:
                self.fp.seek(s[0])
                s=self.fp.read(64)
                s=struct.unpack("I1s27s12sII12s",s)
            if s[0]==1 and s[2].strip()!=forum_name:
                return False
            self.fp.seek(s[4])
            y=self.fp.read(128)
            y=struct.unpack("III8s8s12sIIII28sI24s16s",y)


            #print y[0]
            while y[0]!=ques_id and y[9]!=1:
                #print y
                #print y[0]
                self.fp.seek(y[9])
                y=self.fp.read(128)
                y=struct.unpack("III8s8s12sIIII28sI24s16s",y)
            meta_data=[]
            if y[0]!=ques_id and y[9]==1:
                return False


            if y[6]!=1:
                self.fp.seek(y[6])
                y=self.fp.read(128)
                #print len(y)
                t=struct.unpack("IIIIIII12sI24sI56s",y)
                self.fp.seek(t[3])

                meta_data.append((t[0],self.fp.read(t[8])))
                m=time.time()
                while t[10]==ques_id and t[0]!=1:
                    self.fp.seek(t[4])
                    s=self.fp.read(128)
                    t=struct.unpack("IIIIIII12sI24sI56s",s)
                    self.fp.seek(t[3])

                    meta_data.append((t[0],self.fp.read(t[8])))


            return meta_data[:-1]

    def close(self):
        self.fp.close()



Begin()
r=Register()
q=Questions()
s=Forums()
a=Answers()
#c=Category()


"""
def test_cases():
    c=Category()
    print c.create_category()
    f=Forums()
    i=0
    while i<100:
        f.create_forum("2","cs"+str(i),"ravi")
        i+=1
    i=0
    while i<100:
        f.create_forum("4","cat4","ravi")
        i+=1
    i=0
    while i<100:
        f.create_forum("2","xy"+str(i),"ravi")
        i+=1
    i=0
    while i<100:
        f.create_forum("4","catag4","ravi")
        i+=1


    f.close()
    q=Questions()
    i=0
    j=0
    while i<100:
        j=0
        while j<100:
            q.create_question("2","cs"+str(i),"question-2-"+str(j),"ravi",("basic","ques"))
            j+=1
        i+=1

    q.close()
    q=Questions()
    i=0
    j=0
    while i<100:
        j=0
        while j<100:
            q.create_question("2","xy"+str(i),"question-xy-2-"+str(j),"ravi",("basic","ques"))
            j+=1
        i+=1

    q.close()
    f=Forums()

    f.create_forum("5","IIIT","sush")
    f.create_forum("5","abc","bondy")


    f.close()

    q=Questions()
    q.create_question("5","IIIT","Iiit question","bondy",("t1","t2"))
    q.create_question("5","abc","abc question","bondy",("t1","t2"))
    q.create_question("5","IIIT","Iiit question number2","bondy",("t1","t2"))

    print q.get_questions("5","IIIT")

    q.close()

    a=Answers()
    a.create_answer("5","IIIT",40003,"answer1","bondy")
    a.create_answer("5","IIIT",40001,"answerto40000","bondy")
    a.create_answer("5","IIIT",40003,"answer2","bondy")
    a.create_answer("5","IIIT",40001,"answer2to40000","bondy")

    print a.get_answers("5","IIIT",40003)
    #a=Answers()

    i=0
    while i<2000:
        print a.create_answer("2","xy0",20100,"Answer"+str(i),"ravi")
        i+=1
    a.close()


"""
