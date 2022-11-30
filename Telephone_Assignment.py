#!/usr/bin/env python
# coding: utf-8

# In[131]:


pip install pymongo


# In[110]:


from pymongo import MongoClient


# In[111]:


client = MongoClient()


# In[112]:


a=client.list_database_names()
a


# In[113]:


#phone is our database
if "phone" in a:
    print("Phone database is already exists")
    db=client["phone"]
else:
    print("phone database is not exist,so we create one")
    db=client["phone"]


# In[114]:


client.get_database("phone")


# In[115]:


b=db.list_collection_names()
b


# In[116]:


#telephone is our collection name
if "telephone" in b:
    print("There is telephone collection already exists, so we drop and create one")
    db.drop_collection("telephone")
    db.create_collection("telephone")
else:
    print("No collection exist for phone database , so we create new one")
    db.create_collection("telephone")

#we are inserting sample documents into the telephone collection

a=[{'Name':"Sachin","PhoneNo":8698958909,"Place":"Bangalore"},
   {'Name':"Riyaz","PhoneNo":7558958909,"Place":"Mangalore"},
   {'Name':"Maxime","PhoneNo":9447958909,"Place":"Newyork"},
   {'Name':"Erwin","PhoneNo":9756958909,"Place":"Berlin"}]
db.telephone.insert_many(a)


# ### CRUD operations

# In[129]:


def insert():                                                   #function to insert
    print("Enter how many records that you want to insert")
    b=int(input())
    for i in range(b):
        print(f"Enter values for {i+1} document")
        print("Enter name:")
        c=input()
        print("Enter Phone number:")
        d=int(input())
        print("Enter place:")
        e=input()
        f={'Name':c,"Phone":d,"Place":e}
        db.telephone.insert_one(f)



def find():                                                     #function to query
    print("\nYou can find documents using following features")
    print("1.Name\n2.PhoneNo\n3.Place")
    b=int(input())
    print("\n1.To find one documents\n2.To find multiple documents")
    d=int(input())
    if(d==1):
        if(b==1):
            c=input("Enter name\n")
            print(db.telephone.find_one({"Name":c}))
        elif(b==2):
            c=int(input("Enter PhoneNo\n"))
            print(db.telephone.find_one({"PhoneNo":c}))
        elif(b==3):
            c=input("Enter Place\n")
            print(db.telephone.find_one({"Place":c}))
        else:
            print("Invalid input")
    else:
        if(b==1):
            c=input("Enter name\n")
            for i in db.telephone.find({"Name":c}):
                print(i)
        elif(b==2):
            c=int(input("Enter PhoneNo\n"))
            for i in db.telephone.find({"Phone":c}):
                print(i)
        elif(b==3):
            c=input("Enter Place\n")
            for i in db.telephone.find({"Place":c}):
                print(i)
        else:
            print("Invalid input")

def update():                                                   #function to update
    print("\nYou can select documents to which you want to update by using following features")
    print("1.Name\n2.PhoneNo\n3.Place")
    b=int(input())
    
    if b not in [1,2,3]:
        print("Invalid input")
    else:
        print("Enter it")
        if(b==2):
            c=int(input())
        else:
            c=input()

        fer={1:"Name",2:"PhoneNo",3:"Place"}

        print("\nwhat we have to update")
        print("1.Name\n2.PhoneNo\n3.Place")
        d=int(input())

        if(d==2):
            scu={1:"Name",2:"PhoneNo",3:"Place"}
            print("Enter new value")
            e=int(input())
        elif(d in [1,3]):
            scu={1:"Name",2:"PhoneNo",3:"Place"}
            print("Enter new value")
            e=input()
        else:
            print("Enter the new key")                           #if we want to create 'new key,value pair'
            e=input()
            scu={1:"Name",2:"PhoneNo",3:"Place"}
            scu[d]=e
            print("Enter the value for new key")
            e=input()
        
        
        print(scu)
        print(db.telephone.update_one({fer[b]:c},{"$set":{scu[d]:e}}))
            
               
def delete():                                                  #function to delete
    print("\nYou can select documents to which you want to delete by using following features")
    print("1.Name\n2.PhoneNo\n3.Place")
    b=int(input())
    
    if b not in [1,2,3]:
        print("Invalid input")
    else:
        print("Enter it")
        if(b==2):
            c=int(input())
        else:
            c=input()
        fer={1:"Name",2:"PhoneNo",3:"Place"}
        
        db.telephone.delete_one({fer[b]:c})
        
    
print("You can Perform Following operation")
print("1.Insert\n2.Find\n3.Update\n4.Delete")
a=int(input())                                  #Take valid input
if(a==2):
    find()
    
if(a==3):
    update()
    
if(a==4):
    delete()
    
if(a==1):
    insert()
    
if a not in [1,2,3,4]:
    print("Invalid input")
    


# In[130]:


for i in db.telephone.find():      #Just to check Reflection of CRUD operations on given collection of documents
    print(i)


# In[ ]:




