import tkinter as tk
from api import get_next_buses
import config

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")

# Frame to contain the lines (kept global so we can clear/repopulate it)
frame = tk.Frame(root, bg="black")
frame.pack(expand=True, fill='both')

def render_buses():
    """Fetch next buses and repopulate the `frame`.

    This function clears the existing widgets then creates one row per bus.
    It schedules itself to run again in 30s.
    """
    # clear existing rows
    for w in frame.winfo_children():
        w.destroy()

    try:
        buses = get_next_buses(config.STOP_ID, 5, 30)
    except Exception as e:
        err_lbl = tk.Label(frame, text=f"Error fetching buses: {e}", fg="red", bg="black")
        err_lbl.pack(padx=20, pady=20)
        # retry after 30s even on error
        root.after(30000, render_buses)
        return

    font_size = 40
    for bus in buses:
        mode = bus[0]          # scheduled / estimated
        line = bus[1]          # número (ex: 1120)
        destination = bus[2]   # destino
        time_string = bus[3]   # ex: "4 Min"
        color = bus[4]         # cor da linha da Carris

        time_color = "green" if mode == "estimated" else "white"
        display_time = " ⌯⌲ " + time_string if mode == "estimated" else time_string

        row = tk.Frame(frame, bg="black")
        # make the row fill the available width so the right-packed time label sits at the edge
        row.pack(fill='x', padx=40, pady=10)

        # left container holds number + destination together on the left
        left = tk.Frame(row, bg="black")
        left.pack(side="left", fill='x', expand=True)

        tk.Label(left, text=line, fg=color, bg="black", font=("Repetition Scrolling", font_size)).pack(side="left")
        # destination immediately after the number, left-aligned
        tk.Label(left, text=" " + destination, fg="white", bg="black", font=("Repetition Scrolling", font_size)).pack(side="left")

        # time stays at the far right of the row
        tk.Label(row, text=" " + display_time, fg=time_color, bg="black", font=("Repetition Scrolling", font_size)).pack(side="right")

        # schedule next refresh in 30 seconds (30000 ms)
        root.after(30000, render_buses)


# initial population and start the periodic refresh
render_buses()

root.bind("<Escape>", lambda e: root.destroy())
root.mainloop()
