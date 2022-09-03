import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from googletrans import Translator
from os.path import join, dirname, abspath
import math
import os


def replace_symbols(file):
    with open(file, 'r') as afile:
        filedata = afile.read()
    filedata = filedata.replace('：', ':')
    filedata = filedata.replace('-> ', ' --> ')
    with open(file, 'w') as afile:
        afile.write(filedata)


def open_text_file():
    # file type
    filetypes = (
        ('srt files', '*.srt'),
        ('text files','*.txt'),
        ('All files', '*.*')
    )

    # show the open file dialog
    fin = fd.askopenfile(filetypes=filetypes)
    if fin:
        print(fin.name)
        # clear _cn, and _temp file content
        open(fin.name[:-4] + "_cn" + fin.name[-4:], 'w').close()
        open(fin.name[:-4] + "_temp" + fin.name[-4:], 'w').close()

    fout = open(fin.name[:-4] + "_cn" + fin.name[-4:],'a')
    # outfilename = dirname(abspath(f))
    # print(outfilename)
    ftemp = open(fin.name[:-4] + "_temp" + fin.name[-4:], 'a+')

    temp=0
    current_block=0
    total_blocks = math.ceil(len(fin.readlines())/50)
    fin.seek(0)

    for line in fin.readlines():
        temp = temp+1
        ftemp.write(line)
        if temp == lines_per_block:
            ftemp.seek(0)
            fcontent = ftemp.read()
            translate = Translator()
            output = translate.translate(fcontent, dest='zh-cn')
            fout.write(output.text)      # write to new file
            fout.write('\n')
            temp = 0
            ftemp.close()
            open(fin.name[:-4] + "_temp" + fin.name[-4:], 'w').close()
            ftemp = open(fin.name[:-4] + "_temp" + fin.name[-4:], 'a+')
            current_block = current_block + 1
            print(round(current_block / total_blocks * 100,1))
            progress(current_block/total_blocks*100)
            print(current_block,'/',total_blocks,' block finished\n')
        else:
            pass

    #finish last block
    ftemp.seek(0)
    fcontent = ftemp.read()
    translate = Translator()
    output = translate.translate(fcontent, dest='zh-cn')
    fout.write(output.text)      # write to new file
    progress(100)
    print(current_block+1,'/',total_blocks,' blocks finished\n')
    print('all done\n')
    showinfo(message='Translation done!')

    fin.close()
    fout.close()
    ftemp.close()
    #remove temp file
    os.remove(fin.name[:-4] + "_temp" + fin.name[-4:])

    replace_symbols(fin.name[:-4] + "_cn" + fin.name[-4:])

    root.update()


def open_button_event():
    th = threading.Thread(target = open_text_file())
    th.start()


def progress(value):
    if pb['value'] < 100:
        pb['value'] = value
        root.update()
    else:
        pass


# Root window
root = tk.Tk()
root.title('SRT translator')
root.resizable(True, True)
root.geometry('600x200')
counter_lines = 0
lines_per_block = 50
try:
    root.iconbitmap("riding.ico")
except:
    print('icon not found\n')

# open file button
s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 10, 'bold'))
open_button = ttk.Button(
    root,
    text='Open SRT File',
    style='my.TButton',
    command=open_button_event
    )
open_button.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

# progressbar
pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=280
)
pb.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

# mainloop
root.mainloop()
