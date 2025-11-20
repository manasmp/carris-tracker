import config
import requests
import api

stops = api.get_stops()
buses = api.get_all_buses()

def search_stops(name):
    """Search for stops matching the given name (case insensitive). Returns a list of tuples (id, name)."""
    results = []
    name_lower = name.lower()
    for stop in stops:
        stop_name = stop.get("name", "")
        if name_lower in stop_name.lower():
            results.append((stop.get("id"), stop_name, stop.get("municipality_name")))
    return results
def pretty_stop_info(stopid):
    """Returns a pretty string for a stop tuple (id, name, municipality,bus number and header)."""
    final = []
    stop = api.get_stop_info(stopid)
    final.append(stopid)
    final.append(stop.get("name"))
    final.append(stop.get("municipality_name"))
    # Add bus numbers serving this stop
    for patternid in stop.get("patterns"):
        final.append((api.get_pattern_line_id(patternid), api.get_pattern_headsign(patternid)))

    return final

def show_search_results(name):
    results = search_stops(name)
    final = []
    n = 0
    for stop in results:
        n += 1
        final.append(("RESULTADO " + str(n), pretty_stop_info(stop[0])))
    print("Total results found: ", n)
    return final

def search():
    name = input("Enter stop name to search: ")
    busid = input("Enter bus number to search: ")
    results = show_search_results(name)  ##OPTMIZE THIS LATER
    for res in results:
        for bus in res[1][3:]:
            if bus[0] == busid:
                print("Found bus ", busid, " at stop ", res[1][1])
                return res[1][0]
print(search())