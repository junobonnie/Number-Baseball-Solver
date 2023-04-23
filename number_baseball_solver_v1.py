# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 21:42:27 2023

@author: replica
"""
import os
from PIL import Image
import tkinter
import tkinter.messagebox
import customtkinter
from number_baseball import *

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # 숫자야구에 사용될 숫자들
        self.numbers = list(range(0,10))
        
        # 숫자야구할때 숫자의 길이
        self.length = 3
        self.bb = Baseball(self.numbers, self.length)
        self.bold_font = customtkinter.CTkFont(size=20, weight="bold")
        #print(self.lists)
        
        
        self.dark_mode_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "sun-fill.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "moon-stars-fill.png")), size=(20, 20))
        
        self.restart_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "arrow-clockwise.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "arrow-clockwise-white.png")), size=(30, 30))
        
        self.dark_mode = True
        
        # configure window
        self.title("Number Baseball Solver")
        self.geometry("610x580")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure((1, 2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Number\nBaseball\nSolver", font=self.bold_font)
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(20, 10))
        
        self.length_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["1", "2", "3", "4", "5"], width = 120, height = 50, font=self.bold_font, text_color = ('black', 'white'),
                                                               command=self.change_length)
        self.length_optionemenu.grid(row=6, column=0, columnspan=2, padx=(10, 5), pady=(10, 0))
        
        self.restart_button = customtkinter.CTkButton(self.sidebar_frame, text = '', width = 120, height = 50, command=self.restart, image = self.restart_image)
        self.restart_button.grid(row=7, column=0, columnspan=2, padx=(10, 5), pady=(10, 0))
      
        self.appearance_mode_button = customtkinter.CTkButton(self.sidebar_frame, text = '', width = 35, height = 35, command=self.change_appearance_mode_event, image = self.dark_mode_image)
        self.appearance_mode_button.grid(row=8, column=0, padx=(10, 5), pady=(10, 10))
        
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], width = 70, height = 35, text_color = ('black', 'white'), 
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=1, padx=5, pady=(10, 10))

        # create candidates frame with widgets
        self.candidates_frame = customtkinter.CTkScrollableFrame(self, width=140, corner_radius=0, fg_color=('gray70', 'gray30'), label_text="Candidates", label_font=self.bold_font)
        self.candidates_frame.grid(row=0, column=1, rowspan=4, padx=(1, 1), sticky="nsew")
        self.candidates_frame.grid_rowconfigure(4, weight=1)
        self.candidates_frame.grid_columnconfigure(1, weight=1)
        
        # create nsmb frame with widgets
        self.nsmb_frame = customtkinter.CTkScrollableFrame(self, width=140, corner_radius=0, fg_color=('gray70', 'gray30'), label_text="nsmb", label_font=self.bold_font)
        self.nsmb_frame.grid(row=0, column=2, rowspan=4, padx=(1, 1), sticky="nsew")
        self.nsmb_frame.grid_rowconfigure(4, weight=1)
        
        # create history frame with widgets
        self.history_frame = customtkinter.CTkScrollableFrame(self, width=140, corner_radius=0, fg_color=('gray70', 'gray30'), label_text="History", label_font=self.bold_font)
        self.history_frame.grid(row=0, column=3, rowspan=4, padx=(1, 1), sticky="nsew")
        self.history_frame.grid_rowconfigure(4, weight=1)
        self.history_label = []
        
        self.start()
        
        # set default values
        
        self.length_optionemenu.set(str(self.length))
        self.scaling_optionemenu.set("100%")

    def change_appearance_mode_event(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            customtkinter.set_appearance_mode("Dark")
        else:
            customtkinter.set_appearance_mode("Light")     

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def start(self):
        # 후보군 생성
        candidates = list(permutations(self.numbers, self.length))
        candidates = list(map(list_to_text,candidates))
        self.lists = self.bb.get_sorted_lists(candidates)
        
        self.candidates_button = []
        self.candidates_progressbar = []
        for i, l in enumerate(self.lists, start=0):
            self.candidates_button.append(customtkinter.CTkButton(self.candidates_frame, text=l[0], width = 70, height = 35, border_width=0, corner_radius=0, text_color=("gray10", "#DCE4EE"), font=self.bold_font, command=lambda i=i: self.change_nsmb(i)))
            self.candidates_button[i].grid(row=1+i, column=0, padx=(2, 1), pady=(2, 2), sticky="nsew")
            
            self.candidates_progressbar.append(customtkinter.CTkProgressBar(self.candidates_frame, corner_radius=0, progress_color=('green','dark green') ))
            self.candidates_progressbar[i].grid(row=1+i, column=1, padx=(1, 2), pady=(2, 2), sticky="nsew")
            self.candidates_progressbar[i].set(l[2]/self.lists[0][2])
            if i == 200:
                break
    
    def restart(self):
        widgets = self.candidates_frame.grid_slaves()
        for widget in widgets:
            widget.destroy()
            
        widgets = self.nsmb_frame.grid_slaves()
        for widget in widgets:
            widget.destroy()
            
        widgets = self.history_frame.grid_slaves()
        for widget in widgets:
            widget.destroy()
            
        self.nsmb_frame.configure(label_text = 'nsmb')
        
        self.start()
            
    def change_length(self, new_length: str):
        self.length = int(new_length)
        self.bb = Baseball(self.numbers, self.length)
        
        self.restart()
        
    def change_nsmb(self, index: int):
        widgets = self.nsmb_frame.grid_slaves()
        for widget in widgets:
            widget.destroy()
        self.nsmb_frame.configure(label_text = 'nsmb '+self.lists[index][0])
        self.nsmb_button = []
        self.nsmb_progressbar = []
        for i, (key, value) in enumerate(self.lists[index][1].items(), start=0):
            self.nsmb_button.append(customtkinter.CTkButton(self.nsmb_frame, text=key, width = 70, height = 35, border_width=0, corner_radius=0, text_color=("gray10", "#DCE4EE"), font=self.bold_font, command=lambda index=index, nsmb=key: self.change_candidates(index, nsmb)))
            self.nsmb_button[i].grid(row=1+i, column=0, padx=(2, 1), pady=(2, 2), sticky="nsew")
            
            self.nsmb_progressbar.append(customtkinter.CTkProgressBar(self.nsmb_frame, corner_radius=0, progress_color=('red','dark red') ))
            self.nsmb_progressbar[i].grid(row=1+i, column=1, padx=(1, 2), pady=(2, 2), sticky="nsew")
            self.nsmb_progressbar[i].set(len(value)/len(list(self.lists[index][1].values())[0]))
            if i == 200:
                break            
            
    def change_candidates(self, index: int, nsmb: str):
        widgets = self.candidates_frame.grid_slaves()
        for widget in widgets:
            widget.destroy()
            
        self.history_label.append(customtkinter.CTkLabel(self.history_frame, width = 140, height = 35, fg_color=("blue", "dark blue"), font=self.bold_font, text=self.lists[index][0] + " " + nsmb))
        i = len(self.history_label)-1
        self.history_label[i].grid(row=1+i, column=0, padx=(2, 1), pady=(2, 2), sticky="nsew")
            
        candidates = self.lists[index][1][nsmb]
        self.lists = self.bb.get_sorted_lists(candidates)
        
        self.candidates_button = []
        self.candidates_progressbar = []
        for i, l in enumerate(self.lists, start=0):
            self.candidates_button.append(customtkinter.CTkButton(self.candidates_frame, text=l[0], width = 70, height = 35, border_width=0, corner_radius=0, text_color=("gray10", "#DCE4EE"), font=self.bold_font, command=lambda i=i: self.change_nsmb(i)))
            self.candidates_button[i].grid(row=1+i, column=0, padx=(2, 1), pady=(2, 2), sticky="nsew")
            
            self.candidates_progressbar.append(customtkinter.CTkProgressBar(self.candidates_frame, corner_radius=0, progress_color=('green','dark green') ))
            self.candidates_progressbar[i].grid(row=1+i, column=1, padx=(1, 2), pady=(2, 2), sticky="nsew")
            self.candidates_progressbar[i].set(2**(l[2]-self.lists[0][2]))
            if i == 200:
                break
        
        widgets = self.nsmb_frame.grid_slaves()
        for widget in widgets:
            widget.destroy()
            
        
        


if __name__ == "__main__":
    app = App()
    app.mainloop()