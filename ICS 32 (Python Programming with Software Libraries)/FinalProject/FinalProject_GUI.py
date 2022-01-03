import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import *
#from Profile import Profile, Post
#import ds_client
import socket
import sys
import ds_protocol
import os
from ds_messenger import DirectMessage, DirectMessenger
from tkinter import simpledialog
#from tkinter import * 
#from tkinter import messagebox 
#from NaClProfile import NaClProfile

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._users = []
        #self._posts = DirectMessenger.retrieve_all
        self.selected_user = None
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
        self.current_user = DirectMessenger("168.235.86.101", "aliza123", "michelle")
    
    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        self.set_display_text("")
        index = int(self.users_tree.selection()[0])-1 #selections are not 0-based, so subtract one.
        print(index)
        entry = self._users[index]
        self.selected_user=entry
        #self.main.retrieve_new_msgs()
        x = self.current_user
        for i in x.retrieve_new():
            form = f"Message: {i.message} | Timestamp: {i.timestamp}\n"
            self.set_display_text(form)

        '''
        index = int(self.users_tree.selection()[0])-1 #selections are not 0-based, so subtract one.
        print(index)
        entry = self._users[index]
        self.selected_user=entry
        #self.main.retrieve_new_msgs()
        x = self.current_user
        y = len(x.retrieve_new())
        #print(y)
        if  y > 0:
            #print(x.retrieve_new())
            for i in x.retrieve_new():
                form = f"Message: {i.message} | Timestamp: {i.timestamp}\n"
                self.set_display_text(form)
        #else:
            #self.set_display_text("No new messages from this user.") 
        '''    
        
    
    """
    Returns the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.text_editor.get('1.0', 'end').rstrip()

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        self.text_editor.delete(0.0, 'end')          
        self.text_editor.insert(0.0, text)
        # TODO: Write code to that deletes all current text in the self.entry_editor widget
        # and inserts the value contained within the text parameter.
        
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_users(self, users:list):
         self._users = users[:]
         postid = 1
         for po in self._users:
             self._insert_post_tree(postid, po)
             postid = postid + 1
        
    def set_display_text(self, text:str):
        self.entry_editor.delete(0.0, 'end')          
        self.entry_editor.insert(0.0, text)
        
        # TODO: Write code to populate self._posts with the post data passed
        # in the posts parameter and repopulate the UI with the new post entries. ->->> WHAT DOES THIS MEAN?
        # HINT: You will have to write the delete code yourself, but you can take 
        # advantage of the self.insert_posttree method for updating the posts_tree
        # widget.

    """
    Inserts a single post to the post_tree widget.
    """
    def insert_users(self, users):
        self._users.append(users)
        self._insert_post_tree(len(self._users), users)

    def insert_post(self, post):
        self._posts.append(post)
        self._insert_post_tree(len(self._posts), post)
        #pass


    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.set_text_entry("")
        self._users = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_post_tree(self, id, users):
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(users) > 25:
            users = users[:24] + "..."
        
        self.users_tree.insert('', id, id, text=users)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.users_tree = ttk.Treeview(posts_frame)
        self.users_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.users_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, expand=True)
        
        #editor_frame = tk.Frame(master=entry_frame, bg="red")
        #editor_frame.pack(fill=tk.X, expand=True, anchor = 'n')
        editor_frame = tk.Frame(master=entry_frame, bg="black")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        #editor_frame2 = tk.Frame(master=entry_frame, bg="red")
        #editor_frame2.pack(fill=tk.X, side=tk.LEFT, expand=True, anchor='s')
        #editor_frame2 = tk.Frame(master=entry_frame, bg="blue", height = 100)
        #editor_frame2.pack(fill=tk.X, expand=True, anchor = 'n', pady= 5)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        #self.entry_editor = tk.Canvas(editor_frame, width=480, height = 320)
        #self.entry_editor.grid(row=1, column=120, padx = 5, pady = 5)

        #self.entry_editor = tk.Frame(editor_frame, width=500, height = 150)
        #self.entry_editor.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5, pady=5,anchor='n')

        self.text_editor = tk.Text(editor_frame, width=68, height=7)
        self.text_editor.grid(row = 30, column = 120, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=68, height = 25)# state = DISABLED
        self.entry_editor.grid(row=1, column=120, padx = 5, pady = 5)

        #self.send_text = tk.Text(editor_frame, width=0, bg = 'black')
        #self.send_text.pack(fill=tk.X, side=tk.BOTTOM, expand=True)
        #self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=40)

        text_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.text_editor.yview)
        self.text_editor['yscrollcommand'] = text_editor_scrollbar.set
        text_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, send_callback=None, online_callback = None, add_callback=None, retrieve_all_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._online_callback = online_callback
        self._add_callback = add_callback
        self._retrieve_all_callback = retrieve_all_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using he get() function: 
        self.is_online = tk.IntVar()
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    """
    Calls the callback function specified in the online_callback class attribute, if
    available, when the chk_button widget has been clicked.
    """
    def online_click(self):
        #if self._online_callback is not None:
            #chk_value = self.is_online.get()
            #self._online_callback(chk_value)
        # TODO: Add code that implements a callback to the chk_button click event.
        # The callback should support a single parameter that contains the value
        # of the self.is_online widget variable.
        pass
        

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()
            
    def add_click(self):
            if self._add_callback is not None:
                self._add_callback()

    def retrieve_all_click(self):
        if self._retrieve_all_callback is not None:
            self._retrieve_all_callback()

    #def 
                    
    
    """
    Updates the text that is displayed in the footer_label widget
    """
    def set_status(self, message):
        self.footer_label.configure(text=message)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        send_button = tk.Button(master=self, text="Send", width=20)
        send_button.configure(command= self.send_click) #update command to send function
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        add_button = tk.Button(master=self, text="Add User", width=20)
        add_button.configure(command= self.add_click) #update command to add user function
        add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

        retrieve_button = tk.Button(master=self, text="Retrieve ALL Messages", width=40)
        retrieve_button.configure(command= self.retrieve_all_click) #update command to add user function
        retrieve_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        

        #self.footer_label = tk.Label(master=self, text="Ready.")
        #self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._is_online = False

        # Initialize a new NaClProfile and assign it to a class attribute.
        #self._current_profile = Profile()

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        #self._profile_filename = None
        self.current_user = DirectMessenger("168.235.86.101", "aliza123", "michelle")

    def add_pop(self):
        user_name = simpledialog.askstring("Add User","Please enter the user's name")
        #print(user_name)
        if user_name != None:
            if user_name not in self.body._users:
                self.body.insert_users(user_name)
            else:
                CustomErrors.user_duplicate()

    def retrieve_all_msgs(self):
        x = self.current_user
        '''
        newWindow = Toplevel(main)
        newWindow.title("New Window")
        newWindow.geometry("400x400")

        scroll_frame = tk.Frame(master=newWindow, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)

        #Label(newWindow, text=all_msgs).pack()

        sb = Scrollbar(main)
        sb.pack(side = RIGHT, fill = Y)
        mylist = Listbox(main, yscrollcommand = sb.set)
        '''
        top = Tk()  
        sb = Scrollbar(top)  
        sb.pack(side = RIGHT, fill = Y)  
          
        mylist = Listbox(top, width=50, height=25, yscrollcommand = sb.set )  
          
        for i in x.retrieve_all():
            form = f"From: {i.recipient} | Message: {i.message}"
            mylist.insert(END, form)  
          
        mylist.pack( side = LEFT )  
        sb.config( command = mylist.yview )
        '''
        all_msgs=""
        for i in x.retrieve_all():
            form = f"Message: {i.message} | Timestamp: {i.timestamp}"
            mylist.insert(END, form)

        mylist.pack(side=LEFT)
        sb.config(command = mylist.yview)
                
        #newWindow_scroll = tk.Scrollbar(master=scroll_frame, command=display_text.yview)
        #display_text['yscrollcommand'] = newWindow_scroll.set
        #newWindow_scroll.pack(fill=tk.Y, side=tk.RIGHT, expand=False, padx=0, pady=0)
        '''
            
        
        

    def retrieve_new_msgs(self):
        x = self.current_user
        for i in x.retrieve_new():
            print("From: " + i.recipient + " |", "Message: " + i.message + " |", "Timestamp: " + i.timestamp) 

    
      
    def open_profile(self):
        #filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        #self._profile_filename = filename.name
        #self._current_profile = Profile()
        #if os.path.getsize(self._profile_filename) == 0: #handles the issue of opening an empty file
            #if messagebox.askyesno(title= "EMPTY PROFILE", message= "This file is EMPTY! Do you want to ADD a post or OPEN another file? (WARNING: Selecting 'No' would CLOSE the program)") == False:
                #self.close()
        #else:
            #self._current_profile.load_profile(self._profile_filename) #exception handling
            #self.body.reset_ui()
            #self.body.set_posts(self._current_profile.get_posts())
        pass

            
        #print(self._current_profile.username)

        # TODO: Write code to perform whatever operations are necessary to prepare the UI for
        # an existing DSU file.
        # HINT: You will probably need to do things like load a profile, import encryption keys 
        # and update the UI with posts.
    
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    def checkposts(self): #additional method that supports handling the issue of saving a post that already exists
        #chkpost = []
        #for psts in self.body._posts:
            #chkpost.append(psts['entry'])
        #return chkpost
        pass

    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """ 
    def send_post(self):
        if self.body.get_text_entry() != '': #handling the issue of trying to save an empty post
            post = self.body.get_text_entry()
            if self.body.selected_user != None:
                recipient = self.body.selected_user
                print(recipient)
                self.publish(post, recipient)
                self.body.set_text_entry("")
            else:
                CustomErrors.no_recipient()
            
        else:
            CustomErrors.no_text()

                
    def publish(self, post, recipient):
        self.current_user.send(post, recipient)

         #ds_client.send(self._current_profile.dsuserver, 3021, self._current_profile.username, self._current_profile.password, post.get_entry())
         #ds_client.send(...)

        # TODO: Write code to perform whatever operations are necessary to save a 
        # post entry when the user clicks the save_button widget.
        # HINT: You will probably need to do things like create a new Post object,
        # fill it with text, add it to the active profile, save the profile, and
        # clear the editor_entry UI for a new post.
        # This might also be a good place to check if the user has selected the online
        # checkbox and if so send the message to the server.
        

    """
    A callback function for responding to changes to the online chk_button.
    """
    def online_changed(self, value:bool):
        # TODO: 
        # 1. Remove the existing code. It has been left here to demonstrate
        # how to change the text displayed in the footer_label widget and
        # assist you with testing the callback functionality (if the footer_label
        # text changes when you click the chk_button widget, your callback is working!).
        # 2. Write code to support only sending posts to the DSU server when the online chk_button
        # is checked.
        #self._is_online = value 
        #if value == True:
            #self.footer.set_status("Online")
            #self.is_online = False
        #else:
            #self.footer.set_status("Offline")
            #self.is_online = True
        #print(self._is_online)
        #self.body.set_text_entry("Hello World")
        pass
    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='Menu')
        #menu_file.add_command(label='New', command=self.new_profile)
       # menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, send_callback=self.send_post, add_callback=self.add_pop, retrieve_all_callback = self.retrieve_all_msgs)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

class CustomErrors(tk.Frame):
    def user_duplicate():
        messagebox.showerror(title= "USER ALREADY EXISTS", message= "This user is already on the treeview!")
        
    def no_recipient():
        messagebox.showerror(title= "NO RECIPIENT SELECTED", message= "Please select a user to send the message to.")

    def no_text():
        messagebox.showerror(title= "NO TEXT", message= "Please enter a TEXT before sending a post")

    def no_message():
        messagebox.showerror(title= "NO MESSAGE", message= "No new messages from this user.")
        
if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Messenger")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
