import Tkinter as tk
import tkFileDialog as filedialog
import os
import tkMessageBox as tmb

root = tk.Tk()

# constances 
PROGRAM_NAME = 'Footprint Editor'
file_name = None

# media
new_file_icon = tk.PhotoImage(file='icons/new_file.gif')
open_file_icon = tk.PhotoImage(file='icons/open_file.gif')
save_file_icon = tk.PhotoImage(file='icons/save.gif')
undo_icon = tk.PhotoImage(file='icons/undo.gif')
redo_icon = tk.PhotoImage(file='icons/redo.gif')
cut_icon = tk.PhotoImage(file='icons/cut.gif')
copy_icon = tk.PhotoImage(file='icons/copy.gif')
paste_icon = tk.PhotoImage(file='icons/paste.gif')


# callbacks, functions
def cut():
    content_text.event_generate("<<Cut>>")
    onContentChanged()
    return 'break'

def copy():
    content_text.event_generate("<<Copy>>")
    onContentChanged()
    return 'break'

def paste():
    content_text.event_generate("<<Paste>>")
    onContentChanged()
    return 'break'

def undo():
    content_text.event_generate("<<Undo>>")
    onContentChanged()
    return 'break'

def redo(event=None):
    content_text.event_generate("<<Redo>>")
    onContentChanged()
    return 'break'

def selecAll(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return 'break'

def findText(event=None):
    search_toplevel = tk.Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root) # draw on top of root windown
    search_toplevel.resizable(False, False)
    tk.Label(search_toplevel, text='Find All:').grid(row=0, column=0, sticky=tk.E)
    search_entry = tk.Entry(search_toplevel, width=25)
    search_entry.grid(row=0, column=1, padx=2, pady=2, sticky=tk.EW)
    search_entry.focus_set()
    ignore_case_value = tk.IntVar()
    ignore_case_value.set(1)
    tk.Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky=tk.E, padx=2, pady=2)
    tk.Button(search_toplevel, text='Find All', underline=0, 
             command=lambda: search_output(search_entry.get(), ignore_case_value.get(), 
             content_text, search_toplevel, search_entry)).grid(row=0, column=2, sticky=tk.EW, 
             padx=2, pady=2)
    
    def closeSearchWindow():
        content_text.tag_remove('match', '1.0', tk.END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', closeSearchWindow)
    return 'break'

def search_output(needle, if_ignore_case, content_text, search_toplevel, search_entry):
    content_text.tag_remove('match', '1.0', tk.END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos, nocase=if_ignore_case, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config('match', foreground='red', background='yellow')
    search_entry.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))

def openFile(event=None):
    input_file_name = filedialog.askopenfilename(defaultextension='.txt',
                    filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
        content_text.delete('1.0', tk.END)
        with open(file_name) as file:
            content_text.insert('1.0', file.read())
    onContentChanged()

def writeToFile(file_name):
    try:
        content = content_text.get('1.0', tk.END)
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError, e:
        pass

def saveAs(event=None):
    input_file_name = filedialog.asksaveasfilename(
        defaultextension='.txt', filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
    )
    if input_file_name:
        global file_name
        file_name = input_file_name
        writeToFile(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
    return 'break'

def save(event=None):
    global file_name
    if file_name:
        writeToFile(file_name)
    else:
        saveAs()
    return 'break'

def newFile(event=None):
    root.title("Untitled")
    global file_name
    file_name = None
    content_text.delete('1.0', tk.END)
    onContentChanged()

def displayAboutMessage(event=None):
    tmb.showinfo(
        "About", "{}{}".format(PROGRAM_NAME, "\nTkinter GUI Application\nDevelopment Blueprints")
    )

def displayHelpMessage(event=None):
    tmb.showinfo(
        "Help", "Help Book: \nTkinter GUI Application\nDevelopment Blueprints",
        icon='question'
    )

def exitEditor(event=None):
    if tmb.askokcancel("Quit?", "Really Quit?"):
        root.destroy()

def onContentChanged(event=None):
    updateLineNumbers()
    updateCursorInfoBar()

def updateCursorInfoBar(event=None):
    row, col = content_text.index(tk.INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col)+1)
    info_text = "Line: {} | Column: {}".format(line_num, col_num)
    cursor_info_bar.config(text=info_text)

def show_cursor_info_bar():
    if show_cursor_info.get():
        cursor_info_bar.pack(expand=tk.NO, fill=None, side=tk.RIGHT, anchor=tk.SE)
    else:
        cursor_info_bar.pack_forget()

def getLineNumbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split(".")
        for i in range(1, int(row)):
            output += str(i) + "\n"
    return output

def updateLineNumbers(event=None):
    line_numbers = getLineNumbers()
    linenumber_bar.config(state='normal')
    linenumber_bar.delete('1.0', tk.END)
    linenumber_bar.insert('1.0', line_numbers)
    linenumber_bar.config(state='disabled')

def viewAll(*args):
    content_text.yview(*args)
    linenumber_bar.yview(*args)
    return 'break'

def scroll1(*args):
    scroll_bar.set(*args)
    linenumber_bar.yview_moveto(args[1])
    return 'break'

def highLightLine(interval=100):
    content_text.tag_remove('active_line', '1.0', tk.END)
    content_text.tag_add('active_line', 'insert linestart', 'insert lineend+1c')
    content_text.after(interval, toggleHighlight)

def undoHighLight():
    content_text.tag_remove('active_line', '1.0', tk.END)

def toggleHighlight(event=None):
    if highlight_line.get():
        highLightLine()
    else:
        undoHighLight()

def changeTheme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    fg_color, bg_color = fg_bg_colors.split('.')
    content_text.config(background=bg_color, fg=fg_color)

def showPopupMenu(event=None):
    popup_menu.tk_popup(event.x_root, event.y_root)

# settings
root.title(PROGRAM_NAME)
root.geometry('430x360')

# create menu bar
menu_bar = tk.Menu(root)
# file menu 
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left', 
                      image=new_file_icon, underline=0, command=newFile)
file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left',
                      image=open_file_icon, underline=0, command=openFile)
file_menu.add_command(label='Save', accelerator='Ctrl+S', compound='left',
                      image=save_file_icon, underline=0, command=save)
file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+S', compound='left',
                      image=None, command=saveAs)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt+F4', compound='left',
                      image=None, command=exitEditor)
menu_bar.add_cascade(label='File', menu=file_menu)
# edit menu 
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', compound='left',
                      image=undo_icon, command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound='left',
                      image=redo_icon, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left',
                      image=cut_icon, command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left',
                      image=copy_icon, command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left',
                      image=paste_icon, command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Find', accelerator='Ctrl+F', compound='left',
                      image=None, underline=0, command=findText)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', accelerator='Ctrl+A', compound='left',
                      image=None, underline=7, command=selecAll)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
# view menu 
view_menu = tk.Menu(menu_bar, tearoff=0)
show_line_number = tk.IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label='Show Line Number', variable=show_line_number)
show_cursor_info = tk.IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label='Show Cursor Location at Bottom', variable=show_cursor_info, command=show_cursor_info_bar)
highlight_line = tk.IntVar()
view_menu.add_checkbutton(label='Highlight Current Line', variable=highlight_line, on=1, off=0, 
                        command=toggleHighlight)
themes_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu)

# themes choices
color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}

theme_choice = tk.StringVar()
theme_choice.set('Default')
# add radiobutton menu items
for i in sorted(color_schemes):
    themes_menu.add_radiobutton(label=i, variable=theme_choice, command=changeTheme)
menu_bar.add_cascade(label='View', menu=view_menu)
# about menu 
about_menu = tk.Menu(menu_bar, tearoff=0)
about_menu.add_command(label='About', command=displayAboutMessage)
about_menu.add_command(label='Help', command=displayHelpMessage)
menu_bar.add_cascade(label='About', menu=about_menu)
# add menu bar
root.config(menu=menu_bar)


# create shortcut bar
shortcut_bar = tk.Frame(root, height=25, background='light sea green')
shortcut_bar.pack(expand=tk.NO, fill=tk.X)


# create line number bar 
linenumber_bar = tk.Text(root, width=4, padx=3, takefocus=0, border=0,
                         background='khaki', state='disabled', wrap='none')
linenumber_bar.pack(side=tk.LEFT, fill=tk.Y)


# create content text and scrollbar
content_text = tk.Text(root, wrap='word', undo=1)
content_text.pack(expand=tk.YES, fill=tk.BOTH)
scroll_bar = tk.Scrollbar(content_text)
content_text.config(yscrollcommand=scroll1)
scroll_bar.config(command=viewAll)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
linenumber_bar.config(yscrollcommand=scroll_bar.set)

cursor_info_bar = tk.Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand=tk.NO, fill=None, side=tk.RIGHT, anchor=tk.SE)

# add icons
icons = ('new_file', 'open_file', 'save', 'cut', 'copy', 'paste', 'undo',
        'redo', 'find_text')
commands = ('newFile', 'openFile', 'save', 'cut', 'copy', 'paste', 'undo', 'redo', 'findText')
for i, icon in enumerate(icons):
    tool_bar_icon = tk.PhotoImage(file='icons/{}.gif'.format(icon))
    cmd = eval(commands[i])
    tool_bar = tk.Button(shortcut_bar, image=tool_bar_icon, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side='left')

# create pop-up menu
popup_menu = tk.Menu(content_text, tearoff=0)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound=tk.LEFT, command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7, command=selecAll)

# events binding
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Control-a>', selecAll)
content_text.bind('<Control-A>', selecAll)
content_text.bind('<Control-f>', findText)
content_text.bind('<Control-F>', findText)
content_text.bind('<Control-N>', newFile)
content_text.bind('<Control-n>', newFile)
content_text.bind('<Control-O>', openFile)
content_text.bind('<Control-o>', openFile)
content_text.bind('<Control-s>', save)
content_text.bind('<Control-S>', save)
content_text.bind('<KeyPress-F1>', displayHelpMessage)
content_text.bind('<Any-KeyPress>', onContentChanged)
content_text.tag_config('active_line', background='ivory2')
content_text.bind('<Button-1>', updateCursorInfoBar)
content_text.bind('<Button-3>', showPopupMenu)

root.protocol("WM_DELETE_WINDOW", exitEditor)
root.mainloop()
