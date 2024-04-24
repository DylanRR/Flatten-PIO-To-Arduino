# frontEnd_module.py
import tkinter as tk
from tkinter import filedialog, ttk  # Import ttk
from fileParsing_module import compileProject
import threading

class Application(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.master.title("Arduino Project Compiler")
    self.master.minsize(500, 100)
    self.grid(padx=10, pady=10)
    self.create_widgets()

  def create_widgets(self):
    self.project_name_label = tk.Label(self, text="Project Name")
    self.project_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    self.project_name_entry = tk.Entry(self, width=70)
    self.project_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    # Bind the check_inputs method to the FocusOut event
    self.project_name_entry.bind("<FocusOut>", lambda event: self.check_inputs())

    self.main_dir_button = ttk.Button(self, text="Select Development Folder", command=self.select_main_dir)
    self.main_dir_button.grid(row=1, column=0, sticky="w", padx=5, pady=5)

    self.main_dir_label = tk.Label(self, text="")
    self.main_dir_label.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    self.save_dir_button = ttk.Button(self, text="Select Production Folder", command=self.select_save_dir)
    self.save_dir_button.grid(row=2, column=0, sticky="w", padx=5, pady=5)

    self.save_dir_label = tk.Label(self, text="")
    self.save_dir_label.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    # Create a frame for the compile button
    self.compile_frame = tk.Frame(self)
    self.compile_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Place the compile button in the center of the frame
    self.compile_button = ttk.Button(self.compile_frame, text="Compile", state=tk.DISABLED, command=self.compile)
    self.compile_button.pack()

    self.grid_columnconfigure(1, weight=1)

  def create_listbox_widget(self):
    # Create a frame for the listbox and scrollbar
    self.listbox_frame = tk.Frame(self)
    self.listbox_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    # Create the vertical scrollbar
    self.yscrollbar = tk.Scrollbar(self.listbox_frame, orient='vertical')
    self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create the horizontal scrollbar
    self.xscrollbar = tk.Scrollbar(self.listbox_frame, orient='horizontal')
    self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    # Create the listbox and associate it with the scrollbars
    self.listbox = tk.Listbox(self.listbox_frame, xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)
    self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure the scrollbars to update the listbox view
    self.yscrollbar.config(command=self.listbox.yview)
    self.xscrollbar.config(command=self.listbox.xview)

    self.grid_columnconfigure(1, weight=1)



  def select_main_dir(self):
    self.main_dir = filedialog.askdirectory(title="Select the main directory")
    self.main_dir_label.config(text=self.main_dir)
    self.check_inputs()

  def select_save_dir(self):
    self.save_dir = filedialog.askdirectory(title="Select the directory to save the new project to")
    self.save_dir_label.config(text=self.save_dir)
    self.check_inputs()

  def check_inputs(self):
    # Check if all inputs are set
    if hasattr(self, 'main_dir') and hasattr(self, 'save_dir') and self.project_name_entry.get() != '':
      self.compile_button.config(state=tk.NORMAL)
    else:
      self.compile_button.config(state=tk.DISABLED)

  def compile(self):
    self.project_name = self.project_name_entry.get()
    self.create_listbox_widget()
    self.add_message("Compiling...")
    threading.Thread(target=compileProject, args=(self.main_dir, self.save_dir, self.project_name, self.add_message)).start()

  def add_message(self, message): # Thread-safe, use the after method to schedule the gui update
    self.listbox.after(0, self._add_message, message)

  def _add_message(self, message): # Not thread-safe
    self.listbox.insert(tk.END, message)
    self.listbox.see(tk.END)

def init_gui():
  root = tk.Tk()
  app = Application(master=root)
  app.mainloop()



