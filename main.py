import tkinter as tk
from api import get_next_buses,get_now,get_stop_name
import config
import threading

root = tk.Tk()
# run windowed instead of fullscreen so the app is easier to debug locally
root.title="Carris Tracker"
root.geometry("1280x720")
root.resizable(True, True)
root.configure(bg="black")

# Frame to contain the lines (kept global so we can clear/repopulate it)
frame = tk.Frame(root, bg="black")
frame.pack(expand=True, fill='both')

# add a bottom bar to show the stop street name (left) and current time (right)
bottom_bar = tk.Frame(root, bg="black")
bottom_bar.pack(side="bottom", fill='x')
street_lbl = tk.Label(bottom_bar, text="", fg="white", bg="black", font=("Repetition Scrolling", 20))
street_lbl.pack(side="left", padx=(0, 40), pady=10)
time_lbl = tk.Label(bottom_bar, text="", fg="white", bg="black", font=("Repetition Scrolling", 20))
time_lbl.pack(side="right", padx=25, pady=10)

def render_buses():
    """Start a background thread to fetch buses, then update the UI on the main thread."""
    def worker():
        try:
            buses = get_next_buses(config.STOP_ID, config.NBUSES, config.MINUTESAHEAD)
            stopname = get_stop_name(config.STOP_ID)
            now = get_now()
            # schedule the UI update on the main thread
            root.after(0, lambda: update_ui(buses, stopname, now))
        except Exception as e:
            root.after(0, lambda: show_error(e))

    threading.Thread(target=worker, daemon=True).start()

def update_ui(buses, streetname, time_now):
    # clear existing rows
    for w in frame.winfo_children():
        w.destroy()

    # update bottom corner info once per refresh
    street_lbl.config(text=streetname)
    time_lbl.config(text=time_now)

    font_size = 30
    for bus in buses:
        mode = bus[0]          # scheduled / estimated
        line = bus[1]          # número (ex: 1120)
        destination = bus[2]   # destino
        time_string = bus[3]   # ex: "4 Min"
        color = bus[4]         # cor da linha da Carris

        time_color = "green" if mode == "estimated" else "white"
        display_time = " ⌯⌲ " + time_string if mode == "estimated" else time_string

        row = tk.Frame(frame, bg="black")
        row.pack(fill='x', padx=(0, 40), pady=10)

        left = tk.Frame(row, bg="black")
        left.pack(side="left", fill='x', expand=True)

        tk.Label(left, text=line, fg=color, bg="black", font=("Repetition Scrolling", font_size)).pack(side="left")
        tk.Label(left, text=" " + destination, fg="white", bg="black", font=("Repetition Scrolling", font_size)).pack(side="left")

        tk.Label(row, text=" " + display_time, fg=time_color, bg="black", font=("Repetition Scrolling", font_size)).pack(side="right", padx=25)

    # schedule next refresh in 30 seconds (30000 ms)
    root.after(30000, render_buses)

#idk why i bother! errors dont happen cuz im goated 
def show_error(e):
    for w in frame.winfo_children():
        w.destroy()
    err_lbl = tk.Label(frame, text=f"Error fetching buses: {e}", fg="red", bg="black")
    err_lbl.pack(padx=20, pady=20)
    # keep bottom info updated on error
    street_lbl.config(text="")
    time_lbl.config(text=get_now())
    root.after(30000, render_buses)

# initial population and start the periodic refresh
render_buses()

root.bind("<Escape>", lambda e: root.destroy())
root.mainloop()
