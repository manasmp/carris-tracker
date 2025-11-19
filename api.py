import requests
import time
import config

# Returns the api link for the specified stop
def get_url_realtime(STOP_ID):   
    return config.BASE_URL+"/stops/"+STOP_ID+"/realtime"

# Returns the api link for the specified line id

def get_line_color(ROUTE_ID):
    line = requests.get(config.BASE_URL+"/lines/"+ROUTE_ID).json()
    return line.get("color")

# Returns the present time in unix
def get_now_unix():
    return int(time.time())  #current time in unixtime

# Returns the present time in HH:MM:SS
def get_now():
    # call time.localtime() (not the function object) to get a struct_time
    return time.strftime("%H:%M:%S", time.localtime())

# Returns the unix time to X minutes from now
def minutes_fromnow(x):
    return get_now_unix() + m_to_s(x)

# Returns the scheduled arrival of a bus in unix time
def get_scheduled_unix(i):
    return i.get("scheduled_arrival_unix")

# Returns the estimated arrival (real time) of a bus in unix time
def get_estimated_unix(i):
    return i.get("estimated_arrival_unix")

def get_estimated(i):  # HH:MM
    return i.get("estimated_arrival")

def get_scheduled(i):  # HH:MM
    return i.get("scheduled_arrival")

# Minutes to seconds (unix time calculations are made in seconds)
def m_to_s(m):
    return m*60

#Prints the next n Buses passing by the STOP_ID given
def minutes_until_bus(i):
    now_unix = get_now_unix()
    est_unix = get_estimated_unix(i)
    if est_unix is not None:
        diff = est_unix - now_unix
    else:
        diff = get_scheduled_unix(i) - now_unix

    minutes = max(0, diff // 60)
    return minutes

def str_minutes_left(i):
    minutes = minutes_until_bus(i)
    if minutes <= 1:
        return "A Chegar"
    else:
        return str(minutes) + " Min"

def get_next_buses(STOP_ID,n,t):
    
    """
    Returns a tuple with the next n buses arriving at the specified STOP_ID within t minutes.
    Tuple contains (mode, line number, destination, time left, line color).
    Args:
        STOP_ID (str): The stop identifier to query.
        n (int): Maximum number of buses to print.
        t (int): Lookahead window in minutes.
    Fetches realtime data, filters buses arriving soon, and prints a summary for each.
    """
    data = requests.get(get_url_realtime(STOP_ID)).json()
    j = 0
    buses = []
    for i in data:
        if j == n:
            break
        #if the bus is within 20 minutes from now
        if (get_now_unix() < get_scheduled_unix(i) and minutes_fromnow(t) > get_scheduled_unix(i)): #or get_now_unix() - get_scheduled_unix(i) < m_to_s(1)):
            est = get_estimated(i)
            if est is not None:
                buses.append(("estimated",i["line_id"], i["headsign"],str_minutes_left(i),get_line_color(i["line_id"])))
            else:
                buses.append(("scheduled",i["line_id"], i["headsign"],str_minutes_left(i),get_line_color(i["line_id"])))
            j += 1
    return buses
print(get_next_buses(config.STOP_ID,5,30))