import tkinter as tk
from api import get_next_buses
import config

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")

# Buscar os autocarros
buses = get_next_buses(config.STOP_ID, 5, 30)

# Criar um frame para conter as linhas
frame = tk.Frame(root, bg="black")
frame.pack(expand=True, fill='both')

# Mostrar 1 label por autocarro
for bus in buses:
    mode = bus[0]          # scheduled / estimated
    line = bus[1]          # número (ex: 1120)
    destination = bus[2]   # destino
    time = bus[3]          # ex: "4 Min"
    color = bus[4]         # cor da linha da Carris

    font_size = 40
    # cor do tempo
    time_color = "green" if mode == "estimated" else "white"
    time = " ⌯⌲ " + time if mode == "estimated" else time 
    row = tk.Frame(frame, bg="black")
    # make the row fill the available width so we can push the time label to the right
    row.pack(fill='x', padx=40, pady=10)

    tk.Label(row, text=line, fg=color, bg="black", font=("Repetition Scrolling", font_size)).pack(side="left")
    tk.Label(row, text=" " + destination, fg="white", bg="black", font=("Repetition Scrolling", font_size)).pack(side="left")
    # pack the time label to the right so it aligns with the screen edge
    tk.Label(row, text=" " + time, fg=time_color, bg="black", font=("Repetition Scrolling", font_size)).pack(side="right")

root.bind("<Escape>", lambda e: root.destroy())
root.mainloop()
