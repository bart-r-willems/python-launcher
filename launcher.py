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
import csv, os, shutil, subprocess, tomllib
from pathlib import Path

class MyTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = read_config("config.toml")
        self.env_path = Path(self.config["paths"]["env"])
        self.env_list = sorted(self.env_path.iterdir())
        self.app_list = self.config["apps"]
        self.fld_list = get_favorites(self.config["paths"]["fav"])

        self.setup_window()
        self.add_widgets()
        self.populate_widgets()

    def setup_window(self):
        self.title("Python Interactive Starter")
        self.geometry("600x400")

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)

    def add_widgets(self):
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.grid(column=1, row=3, columnspan=3, sticky="ESW", padx=5, pady=5)

        # add labels and lists
        self.lbl_env = ttk.Label(self, text="Environment")
        self.lbl_env.grid(row=1, column=1, padx=2, sticky="w")
        self.lst_env = ttk.Treeview(self, show="tree")
        self.lst_env.grid(row=2, column=1, padx=2, sticky="news")

        self.lbl_fld = ttk.Label(self, text="Directory")
        self.lbl_fld.grid(row=1, column=2, padx=2, sticky="w")
        self.lst_fld = ttk.Treeview(self, show="tree")
        self.lst_fld.grid(row=2, column=2, padx=2, sticky="news")

        self.lbl_app = ttk.Label(self, text="Application")
        self.lbl_app.grid(row=1, column=3, padx=2, sticky="w")
        self.lst_app = ttk.Treeview(self, show="tree")
        self.lst_app.grid(row=2, column=3, padx=2, sticky="news")

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
        app_cmd = self.app_list[app]

        full_env = self.env_path / env
        full_path = self.fld_list[fld]["path"]
        if len(app_cmd.split()) == 1:
            cmd = self.env_path / env / "Scripts" / app_cmd
        else:
            cmd = app_cmd.split()
            cmd[0] = self.env_path / env / "Scripts" / cmd[0]

        subprocess.Popen(cmd, cwd=full_path)
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

def read_config(filename):
    with open(filename, mode="rb") as fh:
        return tomllib.load(fh)

if __name__ == "__main__":
    main()
    # print(get_favorites())