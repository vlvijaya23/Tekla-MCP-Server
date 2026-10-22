import uuid
import tkinter as tk
from tkinter import messagebox

machine_id = str(
    uuid.getnode()
)

root = tk.Tk()

root.withdraw()

messagebox.showinfo(
    "Machine ID",
    machine_id
)