""" @name Trackers List Merger
    @version 0.0.1
    @description Helps to quickly merge multiple trackers lists into one specially merged list. Warm regards, LiTBRo! ;)
    @author LiTBRo
    @source https://github.com/LiT-BRo
    @date 03 Feb 2022
"""

from tkinter import *
from tkinter import filedialog
from os import path

import win32gui, win32con
hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

############### GLOBAL-VARIABLES ######
active_files_list = []
trackers_list = []
added_files_no = 0
#######################################

def file_write(file_dir):
    global trackers_list
    with open(file_dir, "a") as f:
        for tracker in trackers_list:
            f.write(str(tracker)+"\n")
    dummy_term_updater(4)

def file_counter_checker():
    org_file_dir = path.normpath(path.expanduser("~/Desktop"))+"\\Trackers_List.txt" #Original
    counter = 1
    if path.exists(org_file_dir) == True: #Check for duplicates
        temp_dir = org_file_dir.split('.')
        file_dir = org_file_dir
        while True:
            if path.exists(file_dir):
                file_dir = temp_dir[0]+f" ({counter})."+temp_dir[1]
                counter += 1
                pass
            else:
                file_write(file_dir)
                break
    else:
        file_write(org_file_dir)

################ BUTTON-FUNCTIONS #####
def clear_button():
    global active_files_list, trackers_list, added_files_no, canvas, workspace, yscrollbar
    active_files_list = trackers_list = []
    added_files_no = 0
    #Filenames-Screen Clear
    main_board.destroy(); filenames_screen()
    #Dummy Terminal Screen Clear
    canvas.destroy(); workspace.destroy(); yscrollbar.destroy(); dummy_terminal_screen(); dummy_term_updater(6)
    
def execute_button():
    if added_files_no >= 2:
        file_counter_checker()
    else: #ERROR - No/One File Exec
        dummy_term_updater(3)

def open_file_button():
    global added_files_no, active_files_list, trackers_list
    filepath = filedialog.askopenfilename(title="Open a Text File", 
      filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    # Extract Filename from path
    # ADD IF CLAUSE TO CHECK IF PATH (FILE) EXSISTS THEN CONTINUE< ELSE ERROR
    if filepath != "" and filepath[::-1][:3] == "txt"and filepath not in active_files_list:
        added_files_no += 1
        active_files_list.append(filepath)
        filename = ((filepath[::-1]).split("/")[0])[::-1]
        filenames_scrn_updater(filename) #FILENAMES-SCREEN UPDATE
        dummy_term_updater(1, filename) #DUMMY-TERMINAL UPDATE
        file = open(filepath, 'r')
        temp_list = []
        temp_list.extend(list(set([ele for ele in (file.read()).split("\n")]))) #Trackers Extracted and sorted for duplicates (RAW->FINAL)
        trackers_list.extend([tracker for tracker in temp_list if not trackers_list and tracker != ""])
        file.close()
    elif filepath in active_files_list: # ERROR - Already Exists.
        dummy_term_updater(2)
    else: #ERROR - Empty Direct.
        dummy_term_updater(0)

################ SYSTEM-FUNCTIONS #####
def filenames_scrn_updater(filename):
    global added_files_no
    msg = f"{added_files_no}\t{filename}"
    Label(main_board, text=msg, background='white', font=("Helvetica Bold", 10), padx=20, pady=3, anchor=NW).pack(fill=X)

def dummy_term_updater(cond, *arg, **kwarg):
    if cond == 0:
        Label(workspace, text="Error: Please select a valid file.", background='black', foreground='red', padx=3, pady=3, anchor=NW).pack(fill=X)
    elif cond == 1:
        msg = f"Added '{arg[0]}' | Total Files = {added_files_no}"
        Label(workspace, text=msg, background='black', foreground='#34FF24', padx=3, pady=3, anchor=NW).pack(fill=X)
    elif cond == 2:
        Label(workspace, text="Error: This file was added earlier, please choose a different file.", background='black', foreground='red', padx=3, pady=3, anchor=NW).pack(fill=X)
    elif cond == 3:
        Label(workspace, text="Error: Please add 2 files or more to merge.", background='black', foreground='red', padx=3, pady=3, anchor=NW).pack(fill=X)
    elif cond == 4:
        msg = f'--> Export Complete | Merged Trackers = {len(trackers_list)}'
        Label(workspace, text=msg, background='black', foreground='white', padx=3, pady=3, anchor=NW).pack(fill=X)
    elif cond == 5:
        self_credits = """################ Trackers List Merger | Ver: 0.1 | Auth: LiTBRo ###############"""
        Label(workspace, text=self_credits, background='black', foreground='#34FF24', padx=3, pady=3, wraplength=600, anchor=W).pack(fill=X)

        intro_text = """Instructions:\n1. Add text files with trackers (separated by new line each).\n2. Run the program, processing begins.\n3. Merged textfile is exported to Desktop."""
        for i in intro_text.split("\n"):
            Label(workspace, text=i, background='black', foreground='white', padx=3, pady=3, wraplength=600, anchor=W).pack(fill=X)
    elif cond == 6:
        self_credits = """############## Program Reset | Memory Cleared | Cache Cleared #############"""
        Label(workspace, text=self_credits, background='black', foreground='white', padx=3, pady=3, wraplength=600, anchor=W).pack(fill=X)
        
def scroll_changer():  # Increase Default Value for scroll y-axis so that scroll bar activates beforehand content hides
    a = list(canvas.bbox('all'))
    a[3] += 400
    a = tuple(a)
    return a

#######################################
################# USER-INTERFACE ######
#######################################

root = Tk()
root.title("Trackers List Merger")
root.resizable(0, 0)
root.geometry("500x700")

root_wrapper = LabelFrame(root, background='#263D42')
root_wrapper.pack(fill=BOTH, expand="yes")

################ FILENAMES-SCREEN #####
wrapper1 = Frame(root_wrapper, background="white")
wrapper1.pack(fill=BOTH, expand="yes", padx=12, pady=12)

def filenames_screen():
    global main_board
    main_board = Frame(wrapper1, background="white")
    main_board.pack(fill=BOTH, expand="yes")

    files_label = Label(main_board, text="Added Files:", font=("Helvetica Bold", 22), bg='white')
    files_label.pack(ipadx=13, ipady=5, anchor=NW)
filenames_screen()

################ DUMMY-TERMINAL #######
wrapper2 = Frame(root_wrapper, background='black') #Black to avoid ghosting effect
wrapper2.pack(fill=X, expand="no", padx=0, pady=0)

def dummy_terminal_screen():
    global canvas, yscrollbar, canvas, workspace
    canvas = Canvas(wrapper2, bg="black")
    canvas.pack(side=LEFT, fill=BOTH, expand='yes')

    yscrollbar = Scrollbar(wrapper2, orient="vertical", command=canvas.yview)
    yscrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=yscrollbar.set)
    a = canvas.bbox('all')

    canvas.bind('<Configure>', lambda e: canvas.configure(
    scrollregion=scroll_changer()))
    workspace = Frame(canvas, background='blue')
    canvas.create_window((5, 10), window=workspace, anchor="nw")
dummy_terminal_screen()

#######################################
################# FOOTER-BUTTONS ######
#######################################

footer_frame = Frame(root)
footer_frame.pack(side=BOTTOM, expand="no", padx=10, pady=6)

openfile = Button(footer_frame, text="Add File(s)", padx=7,
                  pady=7, fg="white", bg="#263D42", command=open_file_button)
openfile.pack(side=LEFT)

execute = Button(footer_frame, text="Run", padx=15, pady=7,
                 fg="white", bg="#263D42", command=execute_button)
execute.pack(side=LEFT, padx=35)

clear = Button(footer_frame, text="Reset/Clear", padx=7, pady=7,
               fg="white", bg="#263D42", command=clear_button)
clear.pack(side=LEFT)

#######################################
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ FOOTER-BUTTONS ↑↑↑↑↑#
#######################################

dummy_term_updater(5)

root.mainloop()