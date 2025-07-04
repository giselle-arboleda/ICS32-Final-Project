
# a5.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.



import tkinter as tk
from tkinter import ttk, filedialog
from ds_messenger_UPDATE_12_07 import DirectMessage, DirectMessenger

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None, enable_send=None):  #DEBUG
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self.enable_send = enable_send  #DEBUG

        # a list of the recipient objects available in the active DSU file
        self._recipients = []
        self._msgs = []
        self.current_recipient = ''
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    """
    Update the entry_editor with the full recipient entry when the corresponding node in the recipients_tree
    is selected.
    """
    def node_select(self, event):
        self.enable_send()  #DEBUG
        self.set_text_display("")
        index = int(self.recipients_tree.selection()[0])
        self.current_recipient = self._recipients[index]
        entry = ''
        msg_lst = self.current_recipient['messages']
        if len(msg_lst) >= 7:
            msg_lst = self.current_recipient['messages'][-7:]
        for msg in msg_lst:                
            entry += msg + '\n\n'
        self.set_text_display(entry)
        self.set_text_entry("")

    
    """
    Returns the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()

    def add_text_display(self, text:str, sent=None):
        if sent is True:
            j = tk.RIGHT
        elif sent is False:
            j = tk.LEFT
        self.display.configure(state=tk.NORMAL)
        self.display.insert(tk.END, text)
        self.display.configure(state=tk.DISABLED)

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_display(self, text:str):
        self.display.configure(state=tk.NORMAL)
        self.display.delete(0.0, 'end')
        self.display.insert(0.0, text)
        self.display.configure(state=tk.DISABLED)

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        self.entry_editor.delete(0.0, 'end')
        self.entry_editor.insert(0.0, text)
    
    """
    Populates the self._recipients attribute with recipients from the active DSU file.
    """
    def set_recipients(self, recipients:list):
        self._recipients = recipients
        for recipient in self._recipients:
            self._insert_recipient_tree(self._recipients.index(recipient), recipient)

    """
    Inserts a single recipient to the recipient_tree widget.
    """
    def insert_recipient(self, recipient):
        self._recipients.append(recipient)
        id = len(self._recipients) - 1 #adjust id for 0-base of treeview widget
        self._insert_recipient_tree(id, recipient)


    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.set_text_display("")
        self.entry_editor.configure(state=tk.NORMAL)
        self._recipients = []
        for item in self.recipients_tree.get_children():
            self.recipients_tree.delete(item)

    """
    Inserts a recipient entry into the recipients_tree widget.
    """
    def _insert_recipient_tree(self, id, recipient):
        self.recipients_tree.insert('', id, id, text=recipient['username'])
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        recipients_frame = tk.Frame(master=self, width=250)
        recipients_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.recipients_tree = ttk.Treeview(recipients_frame)
        self.recipients_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.recipients_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="", height=50, width=100)
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        display_frame = tk.Frame(master=entry_frame, height=10, bg="red")
        display_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

                
        editor_frame = tk.Frame(master=entry_frame, bg="red", height=10)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.display = tk.Text(display_frame, width=0, state=tk.DISABLED, height=10)
        self.display.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=0, pady=0)
        
        self.entry_editor = tk.Text(editor_frame, width=0, height=10)
        self.entry_editor.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback

        self._draw()
    

    """
    Calls the callback function specified in the send_callback class attribute, if
    available, when the send_button has been clicked.
    """
    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    """
    Updates the text that is displayed in the footer_label widget
    """
    def set_status(self, message):
        self.footer_label.configure(text=message)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        self.send_button = tk.Button(master=self, text="Send", width=20)
        self.send_button.configure(command=self.send_click, state=tk.DISABLED)  #DEBUG , state=tk.DISABLED
        self.send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""
class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._current_profile = DirectMessenger()

        # Initialize a new NaClProfile and assign it to a class attribute.

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        
    """
    Creates a new DSU file when the 'New' menu item is clicked.
    """
    def new_profile(self):
        self.body.reset_ui()
        filename = tk.filedialog.asksaveasfile(defaultextension=".dsu", filetypes=[('Distributed Social Profile', '*.dsu')])
        self._profile_filename = filename.name
        self._current_profile.username = 'WowWowWubbzy'
        self._current_profile.password = 'ILikeMoney123'
        
    
    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self):
        self.body.reset_ui()
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        self._profile_filename = filename.name
        self._current_profile = DirectMessenger()
        self._current_profile.load_profile(self._profile_filename)
        self.body.reset_ui()
        self.body.set_recipients(self._current_profile.get_recipients())
    
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self._current_profile.save_profile(self._profile_filename)
        self.root.destroy()

    """
    sends the text currently in the entry_editor widget to the active DSU file.
    """
    def send_msg(self):
        entry = self.body.get_text_entry()
        self.publish(entry)
        self._current_profile.save_profile(self._profile_filename)
        self.body.add_text_display('You: ' + entry + '\n\n')
        msgs = self._current_profile.retrieve_new()
        entry = ''
        for msg in msgs:
            entry += 'Incoming: ' + msg['message'] + '\n\n'
        if msgs:
            self.body.add_text_display(entry)
        self.body.set_text_entry("")



    def publish(self, entry):
        '''
        Method used by send_msg method for sending to other users.
        '''
        server = "168.235.86.101"
        port = 3021
        self._current_profile.send(entry, self.body.current_recipient['username'])



    def close_win(self, top):
       top.destroy()
       
    def insert_val(self, entry, top):
        recipient = entry.get()
        self._current_profile.add_recipient(recipient)
        self._current_profile.save_profile(self._profile_filename)
        recipient = self._current_profile._recipients[-1]
        self.body.insert_recipient(recipient)
        self.close_win(top)


    def add_user(self):
        top= tk.Toplevel(self)
        top.geometry("750x250")
        #Create an Entry Widget in the Toplevel window
        entry= tk.Entry(top, width= 25)
        entry.pack()
        #Create a Button to print something in the Entry widget
        tk.Button(top,text= "Insert", command= lambda:self.insert_val(entry, top)).pack(pady= 5,side=tk.TOP)

    def color_mode_on(self):
        '''
        Turning Night Mode On
        '''
        green = '#91C286'
        red = '#D15656'
        white = 'white'
        self.footer.config(bg=red)
        self.footer.footer_label.config(bg=green)
        self.footer.send_button.config(bg = green)
        self.body.display.config(bg = red)
        self.body.entry_editor.config(bg = green)
        #self.body.recipients_tree.config(bg = red)
    def color_mode_off(self):
        '''
        Turning Night Mode Off
        '''
        main_color = "white"
        self.footer.config(bg=main_color)
        self.footer.footer_label.config(bg=main_color)
        self.footer.send_button.config(bg = main_color)
        self.body.config(bg = main_color)
        self.body.display.config(bg = main_color)
        self.body.entry_editor.config(bg = main_color)
        pass

    def enabling_send(self):
        self.footer.send_button.configure(state=tk.NORMAL)  #DEBUG

    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File/Settings')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        menu_file.add_command(label='Add User', command=self.add_user)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar.

        #Creating a "Flourish" feature --> Night Mode
        menu_file.add_command(label='Christmas Mode On', command=self.color_mode_on)
        menu_file.add_command(label='Christmas Mode Off', command=self.color_mode_off)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, enable_send=self.enabling_send)  #DEBUG
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        

        self.footer = Footer(self.root, send_callback=self.send_msg)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

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
