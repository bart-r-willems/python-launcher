# launcher.py
"""GUI to launch interactive Python environments"""

# -----------------------------------------------------------------------
# external dependencies
# -----------------------------------------------------------------------
# (none)
# -----------------------------------------------------------------------

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as Filedialog
import tkinter.messagebox as Messagebox
import tkinter.simpledialog as Simpledialog
import csv, os, shutil, subprocess
from pathlib import Path

ENV_PATH = Path("D:\\Python\\Venv")
FAV_PATH = Path("D:\\Python\\Scripts\\notebook_favs.csv")
ROOT_FLD = Path("D:\\Python")

class MyTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env_list = sorted(ENV_PATH.iterdir())
        self.app_list = {"Python": "PYTHON.EXE", 
                         "Jupyter": "JUPYTER-LAB.EXE",
                         "Marimo": "MARIMO.EXE",
                         "IDLE": "IDLE.EXE"}
        self.fld_list = get_favorites(FAV_PATH)

        self.setup_window()
        self.add_widgets()
        self.populate_widgets()

    def setup_window(self):
        self.title("Python Interactive Starter")
        self.geometry("600x400")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def add_widgets(self):
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.grid(row=99, columnspan=3, sticky="ESW", padx=5, pady=5)

        # add labels and lists
        self.lbl_env = ttk.Label(self, text="Environment")
        self.lbl_env.grid(row=1, column=1, padx=2, sticky="w")
        self.lst_env = ttk.Treeview(self, show="tree")
        self.lst_env.grid(row=2, column=1, padx=2, sticky="new")

        self.lbl_fld = ttk.Label(self, text="Directory")
        self.lbl_fld.grid(row=1, column=2, padx=2, sticky="w")
        self.lst_fld = ttk.Treeview(self, show="tree")
        self.lst_fld.grid(row=2, column=2, padx=2, sticky="new")

        self.lbl_app = ttk.Label(self, text="Application")
        self.lbl_app.grid(row=1, column=3, padx=2, sticky="w")
        self.lst_app = ttk.Treeview(self, show="tree")
        self.lst_app.grid(row=2, column=3, padx=2, sticky="new")

        # add the ok and cancel buttons
        self.btn_cancel = ttk.Button(self.btn_frame, text="Cancel")
        self.btn_cancel.pack(side=tk.RIGHT)
        self.btn_cancel.configure(command=self.on_cancel_click)
        self.btn_ok = ttk.Button(self.btn_frame, text="OK")
        self.btn_ok.pack(side=tk.RIGHT)
        self.btn_ok.configure(command=self.on_ok_click)

    def populate_widgets(self):
        for env in self.env_list:
            self.lst_env.insert("", tk.END, text=env.name)
        for fld in self.fld_list:
            self.lst_fld.insert("", tk.END, text=fld)
        for app in self.app_list:
            self.lst_app.insert("", tk.END, text=app)

    def on_cancel_click(self, *args):
        self.destroy()

    def on_ok_click(self, *args):
        env = self.get_selection(self.lst_env)
        fld = self.get_selection(self.lst_fld)
        app = self.get_selection(self.lst_app)

        full_env = ENV_PATH / env
        full_path = self.fld_list[fld]["path"]
        full_app = ENV_PATH / env / "scripts" / self.app_list[app]

        subprocess.Popen(f'"{full_app}"', cwd=full_path)
        self.destroy()

    def get_selection(self, treeview):
        index = treeview.selection()
        return treeview.item(index, "text")
    
def main():
    app = MyTk()
    app.mainloop()

def get_favorites(filename="notebook_favs.csv"):
    with open(filename, 'r', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        favs = {data["title"]:data for data in reader}
    for data in favs.values():
        data["usage"] = int(data["usage"])
    # sort the favorites
    titles = list(favs.keys())
    titles.sort(reverse=True, key=lambda title: favs[title]["usage"])
    return favs    

import subprocess
import os
from pathlib import Path

def run_in_venv(venv_path, executable, args=None, cwd=None):
    """
    Run an executable in a Python virtual environment.
    
    Args:
        venv_path: Path to the virtual environment
        executable: The executable/script to run
        args: Optional list of arguments for the executable
        cwd: Optional working directory (defaults to venv_path)
    """
    venv_path = Path(venv_path).resolve()
    
    # Determine the activation script and Python paths based on OS
    if os.name == 'nt':  # Windows
        python_exec = venv_path / 'Scripts' / 'python.exe'
        activate_script = venv_path / 'Scripts' / 'activate.bat'
    else:  # Unix/Linux/macOS
        python_exec = venv_path / 'bin' / 'python'
        activate_script = venv_path / 'bin' / 'activate'
    
    # Set working directory
    working_dir = cwd if cwd else venv_path
    
    # Build command
    cmd = ["cmd /c", activate_script, executable]
    if args:
        cmd.extend(args)
    
    # Run the process
    print("Running the subprocess")
    print("cwd:", cwd)
    print("commands:", cmd)
    result = subprocess.run(
        cmd,
        cwd=working_dir,
        capture_output=True,
        text=True
    )
    
    return result

if __name__ == "__main__":
    main()
    # print(get_favorites())