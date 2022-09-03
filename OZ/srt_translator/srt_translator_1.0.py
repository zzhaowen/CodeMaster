import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from googletrans import Translator
from os.path import join, dirname, abspath

# Root window
root = tk.Tk()
root.title('SRT translator')
root.resizable(False, False)
root.geometry('1016x600')
counter_lines = 0
try:
    root.iconbitmap("riding.ico")
except:
    pass

# Text editor
halfwidth = root.winfo_screenwidth()//30
text1 = tk.Text(root, width=halfwidth, height=30)
text2 = tk.Text(root, width=halfwidth, height=30)
text1.grid(column=0, row=0, sticky='nsew')
text2.grid(column=1, row=0, sticky='nsew')


def counter_total_translate_lines(file_obj):
    global counter_lines
    for x in file_obj:
        if '-->' in x:
            pass
        elif x.rstrip().isnumeric():  # rstrip remove '/n'
            pass
        elif x in ['\n', '\r\n']:
            pass
        else:
            counter_lines = counter_lines + 1
    print('total lines:',counter_lines)
    return counter_lines


def translate(line):
    if '-->' in line:
        output = line
    elif line.rstrip().isnumeric():  # rstrip remove '/n'
        output = line
    elif line in ['\n', '\r\n']:
        output = line
    else:
        linetranslate = Translator()
        output = linetranslate.translate(line, dest='zh-cn')
        output = output.text +'\n'
    return output


def open_text_file():
    # file type
    filetypes = (
        ('text files', '*.srt'),
        ('All files', '*.*')
    )
    text1.delete(1.0, tk.END)
    text2.delete(1.0, tk.END)
    # show the open file dialog
    f = fd.askopenfile(filetypes=filetypes)
    if f:
        print(f.name)
    fout = open(f.name[:-4] + "_cn" + f.name[-4:],'w')
    # outfilename = dirname(abspath(f))
    # print(outfilename)

    for line in f.readlines():
        output = translate(line)
        fout.write(output)      # write to new file
        text1.insert('end', line)
        text2.insert('end', output)
        text1.see("end")
        text2.see("end")
        root.update()
    f.close()
    fout.close()


def open_button_event():
    th = threading.Thread(target = open_text_file())
    th.start()


# open file button
s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 10, 'bold'))
open_button = ttk.Button(
    root,
    text='Open SRT File',
    style='my.TButton',
    command=open_button_event
    )

open_button.grid(column=0, row=1, columnspan = 2, sticky='nsew', ipadx=0, ipady=30)

root.mainloop()