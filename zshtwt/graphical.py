from tkinter import *
from zshtwt import api_zshtwt
class Window(object):
    def __init__(self):
        self.root_window = Tk()
        
        self.welcomeLabel = Label(self.root_window, text='Welcome to zshtwt.').pack()
       
    def fetch_screen(self, data): #use apizshtwtcomapare
        #below initializing the main logic screen 
        self.nfb_data = data[1] #instance of the contributed data (not following the user back)
        self.unfb_data = data[0] #instance of the contributed data (user not following back)
        self.nfb_data_scroll = Scrollbar(self.root_window)#scrollbar instance of the data of not following user back
        self.nfb_data_scroll.pack()#simply packing the scrollbar
        self.nfb_data_listbox =  Listbox(self.root_window, yscrollcommand=self.nfb_data_scroll.set, selectmode=MULTIPLE)#create the list box for nfb with the option to select multiple entries
        for each in self.nfb_data: #for each user that is not following back our user
            self.nfb_data_listbox.insert(END, str(each)[2:-2])#add that person to the list box
        self.nfb_data_listbox.pack()#pack these changes!
        self.nfb_data_scroll.config(command=self.nfb_data_listbox.yview)#configure the scroll
        self.unfollow_button = Button(self.root_window, text="Unfollow these traitors!", fg="black", bg="red", command=lambda:self.unfollow_and_refresh(self.nfb_staged_data,self.nfb_data_listbox,self.nfb_data_listbox.curselection())).pack()#the button that will fetch the people nfb and deal with that data
        
        self.unfb_data_scroll = Scrollbar(self.root_window)#scrollbar instance of the data of not following user back
        self.unfb_data_scroll.pack()#simply packing the scrollbar
        self.unfb_data_listbox =  Listbox(self.root_window, yscrollcommand=self.unfb_data_scroll.set, selectmode=MULTIPLE)#create the list box for unfb with the option to select multiple entries
        for each in self.unfb_data: #for each 
            self.unfb_data_listbox.insert(END, str(each)[2:-2])#add each of those @s into the listbox of unfb
        self.unfb_data_listbox.pack()#pack that sucker up
        self.unfb_data_scroll.config(command=self.unfb_data_listbox.yview)#configure the scrollbar
        self.follow_them_back_button = Button(self.root_window, text="Follow them back!", fg="white", bg="navy", command=lambda:self.follow_and_refresh(self.unfb_staged_data,self.unfb_data_listbox,self.unfb_data_listbox.curselection())).pack()#the button to top it all off
        
        self.nfb_staged_data = []#initialize empty array to track the clicked
        self.unfb_staged_data = []#initialize empty array to track the clicked
        while True:
            
            for each_nfb in self.nfb_data_listbox.curselection():
                if self.nfb_data[each_nfb] not in self.nfb_staged_data:
                    self.nfb_staged_data.append(self.nfb_data[each_nfb])
            if len(self.nfb_data_listbox.curselection()) != len(self.nfb_staged_data):
                self.nfb_staged_data = []
                
            for each_unfb in self.unfb_data_listbox.curselection():
                if self.unfb_data[each_unfb] not in self.unfb_staged_data:
                    self.unfb_staged_data.append(self.unfb_data[each_unfb])
            if len(self.unfb_data_listbox.curselection()) != len(self.unfb_staged_data):
                self.unfb_staged_data = []
                                                            
            self.root_window.update()
    def follow_and_refresh(self, data, listbox, index):
        api_zshtwt.follow(data)
        for each in index:
            listbox.delete(each)
    def unfollow_and_refresh(self, data, listbox, index):
        api_zshtwt.unfollow(data)
        for each in index:
            listbox.delete(each)
            
    #def execute_upon(self, ):
