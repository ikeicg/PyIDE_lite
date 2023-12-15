import tkinter as tk
from tkinter import *
from tkinter import font, filedialog
import tkinter.scrolledtext as scrolledtext
import subprocess
import re
from tkinter.scrolledtext import ScrolledText

from components.lexer import *
from components.parser import *


process = None

# List to store error positions
error_positions = []

def run_code(event=None):
    code = text_widget.get("1.0", tk.END)
    
    try:
        global process

        # Start the subprocess
        process = subprocess.Popen(
            ["python", "compiler.py", code],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Communicate with the subprocess
        stdout, stderr = process.communicate(input=None)

        # Print the result
        # print('stdout', stdout)
        # print('stderr', stderr)


        #Update the console_box widget

        console_box.config(state=tk.NORMAL)
        console_box.delete("1.0", tk.END)
        console_box.insert(tk.END, stdout)
        if stderr:
            console_box.insert(tk.END, stderr, "error")
        console_box.config(state=tk.DISABLED)
    except Exception as e:
        console_box.config(state=tk.NORMAL)
        console_box.delete("1.0", tk.END)
        console_box.insert(tk.END, f"Error: {str(e)}")
        console_box.config(state=tk.DISABLED)
    
def open_file(event=None):
    global current_file_path
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, code)
            current_file_path = file_path  # Set the current file path
    highlight_keywords()  # Highlight keywords after opening the file

def save_file(event=None):
    global current_file_path
    if current_file_path:
        # If a file path is already set, save to it
        code = text_widget.get("1.0", tk.END)
        with open(current_file_path, "w") as file:
            file.write(code)
    else:
        # If no file path is set, prompt the user to choose a path and save as
        current_file_path = filedialog.asksaveasfilename(filetypes=[("Python Files", "*.py")])
        if current_file_path:
            code = text_widget.get("1.0", tk.END)
            with open(current_file_path, "w") as file:
                file.write(code)

def highlight_keywords(event=None):

    # Clear existing highlighting
    text_widget.tag_remove("variable", "1.0", tk.END)
    text_widget.tag_remove("function", "1.0", tk.END)

    functions_keyword = ['print']

    text_widget.tag_configure("variable", foreground="blue", font=("Courier New", 11, "bold"))
    text_widget.tag_configure("function", foreground="green", font=("Arial Bold", 11, "bold"))

    for line_number, line in enumerate(text_widget.get("1.0", tk.END).splitlines(), start=1):

        # Check if there's a comment symbol (#) in the line
        if '#' in line:
            line = line.split('#')[0]  # Remove the part after the comment symbol

        # matching variables
        for match in re.finditer(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', line):
            start_index = f"{line_number}.{match.start()}"
            end_index = f"{line_number}.{match.end()}"
            text_widget.tag_add("variable", start_index, end_index)

        for func in functions_keyword:
            pattern = r'\b{}\b'.format(re.escape(func))
            for match in re.finditer(pattern, line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                text_widget.tag_add("function", start_index, end_index)


def validate_code():
    global error_positions
    code = text_widget.get("1.0", tk.END)

    # Clear existing error positions
    error_positions = []

    lines = [[i, x] for i, x in enumerate(code.split("\n"), start=1) if x != ""]
    # print(lines)

    # Iterate through each line
    for i, line in lines:
        lexer = Lexer(line, i)
        tokens, error = lexer.tokenize()

        if(error):
            error_positions.append([error.sourcePos, error.errPos])
            continue

        parser = Parser(line, tokens, i)
        try:
            result, error2 = parser.parseTokens()
        except:
            break

        if(error2):
            error_positions.append([error2[0].sourcePos, error2[0].errPos])


    # Highlight error positions in the text widget
    highlight_errors()

    # Re-schedule validation after 500 milliseconds
    root.after(500, validate_code)

def highlight_errors():
    # Clear existing error tags
    text_widget.tag_remove("error_line", "1.0", tk.END)

    # Highlight error positions
    for line, position in error_positions:
        position = position if position != 0 else 1
        if(not line):
            break
        start_index = f"{line}.0"
        end_index = f"{line}.{position}"
        text_widget.tag_add("error_line", start_index, end_index)
        text_widget.tag_configure("error_line", underline=True, foreground='red')


def light():
    text_widget.config(fg="black", bg="white")
    console_box.config(fg="black", bg="white")

    text_widget.tk_setPalette(background="white", foreground="black")
    text_widget.update_idletasks()

def dark():
    text_widget.config(fg="white", bg="#393939")
    console_box.config(fg="white", bg="#393939")

    text_widget.tag_configure("variable", foreground="yellow", font=("Courier New", 11, "bold"))
    text_widget.tag_configure("function", foreground="green", font=("Arial Bold", 11, "bold"))

    text_widget.tk_setPalette(background="#393939", foreground="white")
    text_widget.update_idletasks()


class LineNumbers(Text):
    def __init__(self, master, self_widget, **kwargs):
        super().__init__(master, **kwargs)

        self.self_widget = self_widget
        self.self_widget.bind('<KeyRelease>', self.on_key_release)
        self.self_widget.bind('<KeyPress>', self.on_key_release)
        self.initial_content = self.self_widget.get(1.0, END)

        self.insert(1.0, '1')
        self.configure(state='disabled')
        self.configure(font=font.Font(size=11))

        self.check_content_changes()

    def on_key_release(self, event=None):
        p, q = self.self_widget.index("@0,0").split('.')
        p = int(p)
        final_index = str(self.self_widget.index(END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(p + no) for no in range(int(num_of_lines) - 1))
        width = len(str(num_of_lines))

        self.configure(state='normal', width=width)
        self.delete(1.0, END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')

    def check_content_changes(self):
        # Check for changes in the content of the self_widget
        current_content = self.self_widget.get(1.0, END)
        if current_content != self.initial_content:
            self.on_key_release()
            self.initial_content = current_content  # Update the initial content

        # Schedule the next content check after 500 milliseconds
        self.after(500, self.check_content_changes)


root = tk.Tk()
root.title("Python IDE")


# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a "File" menu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As",command=save_file)


# Theme Widget
theme_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Light", command=light)
theme_menu.add_command(label="Dark", command=dark)

# Run Code
run_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Execute", command=run_code)


# Create a text widget for code input
text_widget: ScrolledText = scrolledtext.ScrolledText(root, height=25, wrap="word", undo=True)
left_rule = LineNumbers(root, text_widget, width=1, height=25)
left_rule.pack(side=LEFT, anchor="nw")
text_widget.pack(expand=True, fill='both')
text_widget.configure(font=("Courier New", 11, "bold"))

# Bind the highlight_keywords function to text modifications
text_widget.bind("<KeyRelease>", highlight_keywords)

# Create a console window for displaying execution output
console_box = scrolledtext.ScrolledText(root, wrap=tk.WORD)
console_box.pack(expand=True, fill='both')
console_box.tag_configure("error", foreground="red")
console_box.config(state=tk.DISABLED)
console_box.configure(font=("Courier New", 11, "bold"))


# Initialize the current file path
current_file_path = None

root.bind('<Control-s>', save_file)
root.bind('<F5>', run_code)
root.bind('<Control-o>', open_file)

# Start code validation every 3 seconds
validate_code()

#Start main loop for Tkinter
try:
    root.mainloop()
except:
    quit()



