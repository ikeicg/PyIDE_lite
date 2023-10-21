import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog  #allows file system controls
import subprocess
import re #regex library

process = None
def run_code():
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
        # print('stdout',stdout)
        # print('stderr', stderr)


        # Update the output_text widget
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, stdout)
        if stderr:
            output_text.insert(tk.END, stderr, "error")
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")
        output_text.config(state=tk.DISABLED)

def open_file():
    global current_file_path
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, code)
            current_file_path = file_path  # Set the current file path
    highlight_keywords()  # Highlight keywords after opening the file

def save_file():
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
    import keyword

    # Clear existing highlighting
    text_widget.tag_remove("keyword", "1.0", tk.END)
    text_widget.tag_remove("function", "1.0", tk.END)
    text_widget.tag_remove("module", "1.0", tk.END)
    text_widget.tag_remove("constant", "1.0", tk.END)

    # List of Python keywords (including "print")
    keywords = keyword.kwlist

    # Separate built-in entities into different lists
    built_in_functions = [
        'abs', 'len', 'range', 'input', 'str', 'int', 'float', 'list', 'tuple',
        'dict', 'set', 'bool', 'print', 'type', 'id', 'dir', 'help', 'enumerate',
        'zip', 'map', 'filter', 'sum', 'max', 'min', 'sorted', 'open', 'file',
        'isinstance', 'super', 'setattr', 'getattr', 'hasattr', 'delattr', 'eval',
        'exec', 'compile', 'globals', 'locals', 'vars', 'globals', 'locals', 'next',
        'iter', 'slice', 'chr', 'ord', 'divmod', 'pow', 'round', 'format',
        'callable', 'repr', 'ascii', 'complex', 'oct', 'bin', 'hex',
    ]

    built_in_modules = [
        'math', 'random', 'os', 'sys', 'json', 'datetime', 'time', 'collections',
        'string', 're', 'io', 'subprocess', 'sqlite3', 'multiprocessing',
        'threading', 'urllib', 'socket', 'csv', 'xml', 'pickle', 'json', 'glob',
        'argparse', 'logging', 'unittest', 'doctest', 'pdb',
    ]

    constants = ['True', 'False', 'None']


    for line_number, line in enumerate(text_widget.get("1.0", tk.END).splitlines(), start=1):

        # Check if there's a comment symbol (#) in the line
        if '#' in line:
            line = line.split('#')[0]  # Remove the part after the comment symbol

        for kw in keywords:
            pattern = r'\b{}\b'.format(re.escape(kw))
            for match in re.finditer(pattern, line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                text_widget.tag_add("keyword", start_index, end_index)
                text_widget.tag_configure("keyword", foreground="red", font=("TkDefaultFont", 10, "bold"))

        for func in built_in_functions:
            pattern = r'\b{}\b'.format(re.escape(func))
            for match in re.finditer(pattern, line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                text_widget.tag_add("function", start_index, end_index)
                text_widget.tag_configure("function", foreground="green", font=("TkDefaultFont", 10, "bold"))

        for module in built_in_modules:
            pattern = r'\b{}\b'.format(re.escape(module))
            for match in re.finditer(pattern, line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                text_widget.tag_add("module", start_index, end_index)
                text_widget.tag_configure("module", foreground="brown", font=("TkDefaultFont", 10, "bold"))

        for const in constants:
            pattern = r'\b{}\b'.format(re.escape(const))
            for match in re.finditer(pattern, line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                text_widget.tag_add("constant", start_index, end_index)
                text_widget.tag_configure("constant", foreground="blue", font=("TkDefaultFont", 10, "bold"))

        for match in re.finditer(r'(["\']).*?\1', line):
            start_index = f"{line_number}.{match.start()}"
            end_index = f"{line_number}.{match.end()}"
            text_widget.tag_add("string", start_index, end_index)
            text_widget.tag_configure("string", foreground="purple", font=("TkDefaultFont", 10, "bold"))


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
file_menu.add_command(label="Save As", command=save_file)

# Create a "Run" menu
run_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Run Code", command=run_code)

# Create a text widget for code input
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_widget.pack(expand=True, fill='both')
text_widget.configure(font=("TkDefaultFont", 10))

# Bind the highlight_keywords function to text modifications
text_widget.bind("<KeyRelease>", highlight_keywords)

# Create a console window for displaying execution output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
output_text.pack(expand=True, fill='both')
output_text.tag_configure("error", foreground="red")
output_text.config(state=tk.DISABLED)


# Initialize the current file path
current_file_path = None

# Start the Tkinter main loop
root.mainloop()
