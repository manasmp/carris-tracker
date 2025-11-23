# carris-tracker

**Warning — very early in development. Expect bugs and breaking changes.**

Carris Metropolitana public bus arrival tracker

## About This Project
I took big inspiration from the [Transit Tracker Project](https://transit-tracker.eastsideurbanism.org/) but instead of using a LED Display, I'll be making a front-end to display on a normal screen like my CRT TV. 
<p align="center">
<img src="https://i.imgur.com/4sxGyGB.png">
</p>

#### Made with: 
 - Python (Tkinter for graphics)
 - [Carris Metropolitana
   API](https://github.com/carrismetropolitana/api)  for real time
   information about the buses.

#### Why ? 
 - I wanted to learn how to interact with APIs, since I've never worked with it before
 - I've had a CRT in my room for years I haven't used in a while. This could also be later added (I hope) to the [Homepage](https://github.com/gethomepage/homepage) I'm selfhosting in my local network as a widget.
<p align="center">
<img  src="https://i.imgur.com/BgBwLDj.png" height=200>
</p>

## How to use

1. Open the project config file and set the stop ID:
   - Edit `config.py` in the project root and set the STOP_ID value:
     ```python
     STOP_ID = "YOUR_STOP_ID"
     ```
   - The STOP_ID can be found on the Carris Metropolitana website — search for the stop and copy the ID from the stop's page URL or the realtime API URL (it appears as the segment after `/stops/`).

2. Install dependencies:
   - ```bash
     sudo apt install python3 python3-tk 
     ```
     if it asks for anything else like time, re or requests, just install it.

3. Run the app:
   - From the project root: `python3 main.py`

Notes:
- The app fetches realtime data for the configured stop. If you change the STOP_ID, restart the app to load the new stop.
- This project is experimental; behavior and ui will change.

#### What I've learned with this:
 - Requesting from [API](https://github.com/carrismetropolitana/api)
 - Simple Multithreading
 - Basic [TKinter](https://docs.python.org/3/library/tkinter.html) UI notions


#### How it Looks
<p align="center">
Currently, main.py generates a screen like this: 
 
<img src="https://i.imgur.com/ufqgLw0.jpeg">
</p>
