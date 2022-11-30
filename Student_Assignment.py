#!/usr/bin/env python
# coding: utf-8

# In[410]:


pip install pymongo


# In[411]:


from pymongo import MongoClient
import json


# In[412]:


client=MongoClient()


# In[413]:


a=client.list_database_names()
a


# In[414]:


#student is our database
if "student" in a:
    print("Student database already exists")
    db=client["student"]
    
else:
    print("Student database does not exist, we are creating one")
    db=client["student"]


# In[415]:


client.get_database("student")


# In[432]:


db.list_collection_names()


# In[417]:


#students is our new collection. if it doesn't exist then we have to create

a=db.list_collection_names()
if "students" not in a:
    db.create_collection("students")
else:
    db.drop_collection("students")   #To avoid adding duplicate entries while we running again and again,we drop the old collection and create new one.
    db.create_collection("students")


# In[418]:


stud = []                                  #Create list of documents
for line in open('https://github.com/sachincmanjrekar/MongoDB/blob/main/students.json', 'r'):
    stud.append(json.loads(line))
stud


# In[419]:


db.students.insert_many(stud)  #insert the list of documents into the collection


# ### 1. Find the student name who scored maximum scores in all (exam, quiz and homework)?

# In[420]:


for i in db.students.aggregate([
    
    {"$unwind":"$scores"},   #unwind scores which is embedded document which contains score of exam,quiz,homework.So 3 documents will be for each original document                                   
                            
    
    {"$group":{"_id":"$_id","total":{"$sum":"$scores.score"}}}, 
                             
                             #Group the documents on "-Id". Then the sum of score of exam, quiz and homework on each student and store in "total" variable
    
    
    {"$sort":{"total":-1}},                                   #sort total score in descending order of "total"
    { "$limit" : 1 }                                          #Only top scorer will be returned
   
]):
    a=i["_id"]
    
db.students.find_one({"_id":a},{"name":1})                     #Get the name of the top scorer


# ### 2. Find students who scored below average in the exam and pass mark is 40%?
# 

# In[421]:


for i in db.students.aggregate([
    {"$unwind":"$scores"},
   {"$match":{"scores.type":"exam"}}, 
    {"$group":{"_id":"$null","AvgExam":{"$avg":"$scores.score"}}},
    {"$sort":{"_id":1}}
]):
    a=i['AvgExam']
print("Averege score in Exam : ",a)         #Average score on Exam.
    
print("****************")
print("Students who scored below average in the exam and pass mark is 40%\n")



for i in db.students.aggregate([
    {"$unwind":"$scores"},
    {"$match":{"scores.type":"exam","scores.score":{"$lte":a,"$gte":40}}},
    {"$sort":{"scores.score":-1}}
    #{"$project":{}}
    
]):
    print(i)


# ### 3. Find students who scored below pass mark and assigned them as fail, and above pass mark as pass in all the categories.

# In[422]:


print("Student who Failed and got below Passing marks which is 40% in all three categories\n")
a=[]
for i in db.students.aggregate([
    {"$unwind":"$scores"},
    {"$match":{"scores.type":{"$in":["exam","quiz","homework"]},"scores.score":{"$lte":40}}},
    {"$group":{"_id":"$_id","size":{"$sum":1}}},
    {"$match":{"size":{"$eq":3}}},
    {"$sort":{"_id":1}}
    
]):
    a.append(i["_id"])

for i in db.students.find({"_id":{"$in":a}},{"name":1}):
    print(i)

print("**************************************")


print("Student who Passed and scored above Passing marks which is 40% in all three categories\n")
b=[]
for i in db.students.aggregate([
    {"$unwind":"$scores"},
    {"$match":{"scores.type":{"$in":["exam","quiz","homework"]},"scores.score":{"$gte":40}}},
    {"$group":{"_id":"$_id","size":{"$sum":1}}},
    {"$match":{"size":{"$eq":3}}},
    {"$sort":{"_id":1}}
    
]):
    b.append(i["_id"])

for i in db.students.find({"_id":{"$in":b}},{"name":1}):
    print(i)


# ### 4. Find the total and average of the exam, quiz and homework and store them in a separate collection.`

# In[423]:


#Total_Avg is our new collection. if it doesn't exist then we have to create

a=db.list_collection_names()
if "Total_Avg" not in a:
    db.create_collection("Total_Avg")
else:
    db.drop_collection("Total_Avg")   #To avoid adding duplicate entries if we run again and again,we drop the old collection and create new one.
    db.create_collection("Total_Avg")


# In[424]:


a=[]

for i in db.students.aggregate([
  {"$unwind":"$scores"},
    {"$group":{"_id":"$_id","Total":{"$sum":"$scores.score"},"Average":{"$avg":"$scores.score"}}},
    {"$sort":{"_id":1}}
]):
    for j in db.students.find({"_id":i["_id"]},{"name":1}):
        i["name"]=j["name"]
        tup=list(i.items())
        tup[1],tup[2],tup[3]=tup[3],tup[1],tup[2]
        res=dict(tup)
        a.append(res)
        print(res)

db.Total_Avg.insert_many(a)
 


# ### 5. Create a new collection which consists of students who scored below average and above 40% in all the categories.

# In[435]:


for i in db.students.aggregate([
    {"$unwind":"$scores"},
   {"$match":{"scores.type":"exam"}}, 
    {"$group":{"_id":"$null","AvgExam":{"$avg":"$scores.score"}}},
    {"$sort":{"_id":1}}
]):
    a=i['AvgExam']
    
print("Average score in exam : ",a)

for i in db.students.aggregate([
    {"$unwind":"$scores"},
   {"$match":{"scores.type":"quiz"}}, 
    {"$group":{"_id":"$null","AvgQuiz":{"$avg":"$scores.score"}}},
    {"$sort":{"_id":1}}
]):
    c=i['AvgQuiz']

print("Average score in quiz : ",c)

for i in db.students.aggregate([
    {"$unwind":"$scores"},
   {"$match":{"scores.type":"homework"}}, 
    {"$group":{"_id":"$null","AvgHomeWork":{"$avg":"$scores.score"}}},
    {"$sort":{"_id":1}}
]):
    d=i['AvgHomeWork']

print("Average score in homework : ",d)

print("\nId of the Students who scored above Passing marks which is 40% in all three categories")
b=[]
for i in db.students.aggregate([
    {"$unwind":"$scores"},
    {"$match":{"scores.type":{"$in":["exam","quiz","homework"]},"scores.score":{"$gte":40}}},
    {"$group":{"_id":"$_id","size":{"$sum":1}}},
    {"$match":{"size":{"$eq":3}}},
    {"$sort":{"_id":1}}
    
]):
    b.append(i["_id"])
print(b)

print("\nremove the student who scored more than Average in exam")
for j in db.students.aggregate([
    {"$unwind":"$scores"},
    {"$match":{"scores.type":"exam","scores.score":{"$gte":a}}},
    {"$sort":{"_id":1}},
    
]):
    if(j["_id"] in b):
        b.remove(j["_id"])

print("Remaining student's ID after removal :",b)

print("\nremove the student who scored more than Average in quiz")
for j in db.students.aggregate([
    {"$unwind":"$scores"},
    {"$match":{"scores.type":"quiz","scores.score":{"$gte":c}}},
    {"$sort":{"_id":1}},
    
]):
    if(j["_id"] in b):
        b.remove(j["_id"])

print("Remaining student's ID after removal :",b)

print("\nremove the student who scored more than Average in homework")
for j in db.students.aggregate([
    {"$unwind":"$scores"},
    {"$match":{"scores.type":"homework","scores.score":{"$gte":d}}},
    {"$sort":{"_id":1}},
    
]):
    if(j["_id"] in b):
        b.remove(j["_id"])

print("Remaining student's ID after removal :",b)


#PassAvg is our new collection. if it doesn't exist then we have to create

a=db.list_collection_names()
if "PassAvg" not in a:
    db.create_collection("PassAvg")
else:
    db.drop_collection("PassAvg")   #To avoid adding duplicate entries if we run again and again,we drop the old collection and create new one.
    db.create_collection("PassAvg")
 
f=[]
for i in db.students.find({"_id":{"$in":b}}):#insert the documents because of the resultant queries will be inserted into the new collection
    print(i)
    f.append(i)

if(len(f)>0):
    db.PassAvg.insert_many(f)
else:
    print("\nThere are no students who score atleast 40% and below Average in all categories")


# ### 6. Create a new collection which consists of students who scored below the fail mark in all the categories.
# `

# In[426]:


#Fail is our new collection. if it doesn't exist then we have to create

a=db.list_collection_names()
if "Fail" not in a:
    db.create_collection("Fail")
else:
    db.drop_collection("Fail")   #To avoid adding duplicate entries if we run again and again,we drop the old collection and create new one.
    db.create_collection("Fail")


# In[427]:


print("Student who scored below Passing marks which is 40% in all three categories\n")
a=[]
b=[]
for i in db.students.aggregate([
    {"$unwind":"$scores"},
    {"$match":{"scores.type":{"$in":["exam","quiz","homework"]},"scores.score":{"$lte":40}}},
    {"$group":{"_id":"$_id","size":{"$sum":1}}},
    {"$match":{"size":{"$eq":3}}},
    {"$sort":{"_id":1}}
    
]):
    a.append(i["_id"])

for i in db.students.find({"_id":{"$in":a}}):
    print(i)
    b.append(i)
    
db.Fail.insert_many(b)


# ### 7. Create a new collection which consists of students who scored above pass mark in all the categories.

# In[428]:


#Pass is our new collection. if it doesn't exist then we have to create

a=db.list_collection_names()
if "Pass" not in a:
    db.create_collection("Pass")
else:
    db.drop_collection("Pass")   #To avoid adding duplicate entries if we run again and again,we drop the old collection and create new one.
    db.create_collection("Pass")


# In[429]:


print("Student who scored above Passing marks which is 40% in all three categories\n")
b=[]
c=[]
for i in db.students.aggregate([
    {"$unwind":"$scores"},
    {"$match":{"scores.type":{"$in":["exam","quiz","homework"]},"scores.score":{"$gte":40}}},
    {"$group":{"_id":"$_id","size":{"$sum":1}}},
    {"$match":{"size":{"$eq":3}}},
    {"$sort":{"_id":1}}
    
]):
    b.append(i["_id"])

for i in db.students.find({"_id":{"$in":b}},):
    print(i)
    c.append(i)

db.Pass.insert_many(c)


# In[ ]:





# In[ ]:




