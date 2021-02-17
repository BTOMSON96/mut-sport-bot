

import random

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf

import pickle

from pymongo import MongoClient

# tokenize sentence and stem the words
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that 
# exists in the sentence
def bow(sentence, words, debug=False):
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if debug:
                    print ("found in bag: %s" % w)

    return (np.array(bag))

def classify(sentence):
    # get classification probabilities
    results = model.predict([bow(sentence, words)])[0]
    # remove predictions below the threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    
    # sort by probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
        
    # return intent and probability tuple
    return return_list


ERROR_THRESHOLD = 0.25



# Chatbot response
def response(sentence):
    results = classify(sentence)
   
                
    doc = db.ai_intents.find_one({'name': results[0][0]})
            
    res = random.choice(doc['responses'])
    return res
        
def load_model():
    # restore data structures
    data = pickle.load( open( "training_data", "rb" ) )

    global words
    global classes 
    
    words = data['words']
    classes = data['classes']
    train_x = data['train_x']
    train_y = data['train_y']
    
    # reset underlying graph data
    tf.reset_default_graph()
    
    # Build a neural network
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)
       
    # load saved model
    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
    model.load('./model.tflearn')
    return model
            


#Creating GUI with tkinter (tkinter a tool that comes with python specifically for GUI)


from tkinter import *
from tkinter import ttk
import tkinter   as tk
import textwrap
from datetime import datetime, time
from PIL import ImageTk, Image
import time
import re
from tkinter import messagebox 
import os
from os import environ

connect = MongoClient(environ['GUICONNECTQUERIES'])
db = connect.Enquiries
ai_enquiries = db.ai_enquiries

#setting current time
now = datetime.now()
current_time = now.strftime(" %H:%M \n")



def send(event):
    
    getmsg = EntryBox.get("1.0",'end-1c').strip()
    msg = textwrap.fill(getmsg,30)
    #EntryBox.delete("0.0",END)
    ChatLog.tag_configure('tag-right',justify='right')

    if msg != '':

       ChatLog.config(state=NORMAL)
       ChatLog.insert(END,'\n ', 'tag-right')
       ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=msg, 
       wraplength=200, font=("Arial", 10), bg="lightblue", bd=4))
       ChatLog.insert(END,'\n ', 'tag-right')
       ChatLog.insert(END, current_time+' ', ("small", "right", "greycolour", 'tag-right'))
       ChatLog.config(foreground="#0000CC", font=("Helvetica", 9))
       ChatLog.insert(END,'\n ')
       ChatLog.window_create(END,  window=Label(ChatLog,image= new_image, text="MutBot:", compound=LEFT))
      
       ChatLog.config(state=DISABLED)
       ChatLog.yview(END)
        
def leave(event):
    
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        
        
        res = response(msg)
        
        time.sleep(4)

        
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END,'\n ')
        ChatLog.window_create(END, window=Label(ChatLog, fg="#000000",text=res, 
        wraplength=200, font=("Arial", 10), bg="#DDDDDD", bd=4, justify="left"))
        ChatLog.insert(END, '\n ')
        ChatLog.insert(END, current_time+' ', ("small", "greycolour", "left"))
        ChatLog.insert(END,'', 'tag-right' )
        ChatLog.config(state=DISABLED)
        
        ChatLog.yview(END) 
        

    
    #else:
        
        #res = "Sorry we do not have answer loaded for your question. \n \nPlease click below to send us your question. We will get back to you as soon as poosible with your answer.\n "
        #ChatLog.insert(END,'\n ')
        #ChatLog.window_create(END,  window=Label(ChatLog,image= new_image, text="MutBot:", compound=LEFT))
        #ChatLog.insert(END,'\n ')
        #ChatLog.window_create(END, window=Label(ChatLog, fg="#000000",text=res, 
        #wraplength=200, font=("Arial", 10), bg="#DDDDDD", bd=4, justify="left"))
        #ChatLog.insert(END,'\n ')
        #ChatLog.window_create(END, window=Button(ChatLog, font=("Verdana",8, 'bold'), text="Contact Us",  bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
        #command= contact))
        
        #ChatLog.insert(END, '\n ')
        #ChatLog.insert(END, current_time+' ', ("small", "greycolour", "left"))
        #ChatLog.insert(END,' ', 'tag-right' )
        
        #ChatLog.config(state=DISABLED)
        #ChatLog.yview(END)

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def contact():

    newwindow =  Toplevel(base)
    newwindow.title("Contact Us")
    newwindow.geometry("290x370")
    newwindow.resizable(width=FALSE, height=FALSE)
    
    txtname = tk.StringVar()
    txtsurname = tk.StringVar()
    txtemail = tk.StringVar()
    txtstudentno = tk.StringVar()
    
    txtmessage = tk.StringVar()

   #Create labels
    ttk.Label(newwindow, text="Name: (*)").grid(
        row=0, column=0, padx=10, pady=10)
    ttk.Label(newwindow, text="Surname: ").grid(
        row=1, column=0, padx=10, pady=10)
    ttk.Label(newwindow, text="Email: (*)").grid(
        row=2, column=0, padx=10, pady=10)
    ttk.Label(newwindow, text="StudentNo: ").grid(
        row=3, column=0, padx=10, pady=10)
    ttk.Label(newwindow, text="Enquiry type: (*)").grid(
        row=4, column=0, padx=10, pady=10)
    ttk.Label(newwindow, text="Message: ").grid(
        row=5, column=0, padx=10, pady=10)    

    #Create text boxes
    ttk.Entry(newwindow, textvariable= txtname ).grid(
        row=0, column=1, padx=10, pady=10)
    ttk.Entry(newwindow, textvariable= txtsurname).grid(
        row=1, column=1, padx=10, pady=10)
    ttk.Entry(newwindow, textvariable= txtemail).grid(
        row=2, column=1, padx=10, pady=10)   
    ttk.Entry(newwindow, textvariable= txtstudentno ).grid(
        row=3, column=1, padx=10, pady=10)       
    
    ttk.Entry(newwindow,textvariable= txtmessage).grid(
        row=5, column=1, padx=10, pady=10, ipady=20)
    
    #Creating combobox and its dropdown list
    n = tk.StringVar()  
    enquirychosen = ttk.Combobox(newwindow, textvariable=n)
    enquirychosen['values'] = ('Sports registration',
                                'Ground location',
                                 'Available sports',
                                 'Fitness Gym',
                                 'Other')
    enquirychosen.grid(
        row=4, column=1, padx=10, pady=10)

    #Set Sports registration as a deafult value  
    enquirychosen.current(0)     

    def contactus():
            
        name = txtname.get()
        email = txtemail.get()
        studentno = txtstudentno.get()

        if name !=''  and email !='' :
                if(re.search(regex, email)):
                        if  studentno.isdigit() == True:

                                connect.Enquiries.ai_enquiries.insert_one({                  
                                "name": txtname.get(),      
                                "Surname": txtsurname.get(),
                                "Email": txtemail.get(),
                                "StudentNo": txtstudentno.get(),
                                "EquiryType": n.get(),
                                "Message": txtmessage.get()})


                                newwindow.destroy()
                                ChatLog.config(state=NORMAL)
                                ChatLog.insert(END,'\n ')
                                ChatLog.window_create(END,  window=Label(ChatLog,image= new_image, text="MutBot:", compound=LEFT))
                                ChatLog.insert(END,'\n ')
                                ChatLog.window_create(END, window=Label(ChatLog, fg="#000000",text="Thank you! Your enquiry have been submitted. We will contact you as soon as possible", 
                                wraplength=200, font=("Arial", 10), bg="#DDDDDD", bd=4, justify="left"))
                                ChatLog.insert(END, '\n ')
                                ChatLog.insert(END, current_time+' ', ("small", "greycolour", "left"))
                                ChatLog.insert(END,'', 'tag-right' )
                                ChatLog.config(state=DISABLED)
        
                                ChatLog.yview(END)  
                        else:
                                messagebox.showerror("Invalid student number", "Your student number must not have characters and must not be less than 7 digits ")

                else:
                         messagebox.showerror("Invalid email", "The email address you provided is not valid")

        else:
                Label(newwindow, text= "Please fill in Mandatory(*) fields.", fg= '#ff0000').grid(
                                                row=8, column=1, padx=10, pady=10)
    
    
    #Send button and cancel button
    ttk.Button(newwindow, text="send", command= contactus).grid(
        row=6, column=0, padx=10, pady=10)
    ttk.Button(newwindow, text="cancel", command= newwindow.destroy).grid(
        row=6, column=1, padx=10, pady=10) 




base = Tk()
base.title("MUT-SPORT CHATBOT")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

  
     
  
  


#Profile picture for a chatbot
img = Image.open("logo.jpg")
resized = img.resize((30,30), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized)

#Icon for main window(MUT-SPORT CHATBOT)
icon_image = Image.open("logo.jpg")
icon_resized = icon_image.resize((50,50), Image.ANTIALIAS)
new_icon = ImageTk.PhotoImage(icon_resized)
base.iconphoto(False, new_icon)




#set window background color
base['background']= '#32de97'

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)


#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set


#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="10", height=2,
                    bd=0, bg="#3c9d9b", activebackground="#32de97",fg='#ffffff' )
SendButton.bind("<ButtonPress>", send)
SendButton.bind("<Leave>", leave)

#Button for contact us
ContactButton =Button(ChatLog, font=("Verdana",8, 'bold'), text="Contact Us",  bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
        command= contact)
ContactButton.pack()


#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="3", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=376,y=6, height=420)
ChatLog.place(x=6,y=6, height=420, width=370)
EntryBox.place(x=6, y=440,  width=265)
SendButton.place(x=275, y=440)

# connect to mongodb and set the Intents database for use
client = MongoClient (environ['GUICONNECTINTENTS'])
db = client.Intents

model = load_model()
base.mainloop()