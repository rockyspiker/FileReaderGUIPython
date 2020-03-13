import tkinter as tk
import tkinter.simpledialog as tksimp
import sys

args = sys.argv[1:]

if (len(args) > 0):
    fname=args[0]
    if (len(args) > 1 and isinstance(args[1], int)):
        window_height=args[1]
    else:
        window_height=20
else:
    fname='yankee.txt'
    window_height=20

window_width=50
window=tk.Tk()
cur_page = 1

def get_pages(fname, view_size):
    lineNum = 1
    text = open(fname, 'r')
    pages = [text.tell()]
    for line in iter(text.readline, ''):
        if (lineNum % view_size == 0):
            pages.append(text.tell())
        lineNum += 1
    pages.insert(0,lineNum) # first element in pages is the amount of lines in file
    return pages

pages = get_pages(fname, window_height)

def disp(fname, view_size, seeker):
    text = open(fname, 'r')
    text.seek(seeker)
    windowText = ''
    for line in range(view_size):
        windowText += text.readline()
    return windowText

def window_title():
    title = str(fname) + ' - Page ' + str(cur_page)
    window.title(title)

def build_window(fname, window_height, window_width):
    window_title()

    scrollbar = tk.Scrollbar(window, orient='horizontal')
    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    text=tk.Text(window, wrap='none', width=window_width,
                 height=window_height+1, xscrollcommand=scrollbar.set)
    text.pack()
    text.insert(1.0, disp(fname, window_height, pages[cur_page]))
    text.config(state='disabled')

    scrollbar.config(command=text.xview)

    def go_top():
        global cur_page
        global pages
        cur_page = 1
        text.config(state='normal')
        text.delete(1.0, tk.END)
        text.insert(1.0, disp(fname, window_height, pages[cur_page]))
        text.config(state='disabled')
        window_title()
    
    def go_up():
        global cur_page
        global pages
        if (cur_page > 1):
            cur_page -= 1
            text.config(state='normal')
            text.delete(1.0, tk.END)
            text.insert(1.0, disp(fname, window_height, pages[cur_page]))
            text.config(state='disabled')
        window_title()
    
    def go_down():
        global cur_page
        global pages
        if (cur_page < len(pages)-1):
            cur_page += 1
            text.config(state='normal')
            text.delete(1.0, tk.END)
            text.insert(1.0, disp(fname, window_height, pages[cur_page]))
            text.config(state='disabled')
        window_title()
    
    def go_bottom():
        global cur_page
        global pages
        cur_page = len(pages)-1
        text.config(state='normal')
        text.delete(1.0, tk.END)
        text.insert(1.0, disp(fname, window_height, pages[cur_page]))
        text.config(state='disabled')
        window_title()
    
    def go_page():
        global cur_page
        global pages
        cur_page = tksimp.askinteger("Page", "Enter page number",parent=text)
        if (cur_page > len(pages)-1):
            go_bottom()
        elif (cur_page < 1):
            go_top()
        else:
            text.config(state='normal')
            text.delete(1.0, tk.END)
            text.insert(1.0, disp(fname, window_height, pages[cur_page]))
            text.config(state='disabled')
            window_title()
        
    def go_quit():
        window.destroy()

    buttons = tk.Frame(window)
    buttons.pack(side=tk.BOTTOM)
    top=tk.Button(window, text='Top', command=go_top)
    top.pack(in_=buttons, side=tk.LEFT)
    up=tk.Button(window, text='Up', command=go_up)
    up.pack(in_=buttons, side=tk.LEFT)
    down=tk.Button(window, text='Down', command=go_down)
    down.pack(in_=buttons, side=tk.LEFT)
    bottom=tk.Button(window, text='Bottom', command=go_bottom)
    bottom.pack(in_=buttons, side=tk.LEFT)
    page=tk.Button(window, text='Page', command=go_page)
    page.pack(in_=buttons, side=tk.LEFT)
    quiter=tk.Button(window, text='Quit', command=go_quit)
    quiter.pack(in_=buttons, side=tk.LEFT)
    
    window.mainloop()

if __name__ == '__main__':
    build_window(fname, window_height, window_width)
