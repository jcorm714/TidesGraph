import requests
from matplotlib import pyplot as plt
import datetime as dt
import argparse as ap


#retreive JSON data from url
def getJSON(start_date):

    #throw an error if start_date is less than 14 days from the current day
    end_date = start_date + dt.timedelta(days=14)
    if end_date > dt.datetime.now():
        raise(Exception("Date out of Range: startdate must be at least 14 day prior to today"))
    
    str_start = start_date.strftime("%Y%m%d")
    str_end = end_date.strftime("%Y%m%d")
    url = f"https://tidesandcurrents.noaa.gov/api/datagetter?begin_date={str_start}&end_date={str_end}&station=8454000&product=water_level&datum=mllw&units=metric&time_zone=gmt&application=web_services&format=json"
    r = requests.get(url)
    return r.json()

#retrieve date entered from the CLI
parser = ap.ArgumentParser()
parser.add_argument("--date", type=str, help="Date in the format YYYY-MM-DD,\n also has to be a minimum of 14 days before today")
args = parser.parse_args()
start_date = dt.datetime.strptime(args.date, '%Y-%m-%d')

data = {}

try:
    data = getJSON(start_date)
except Exception as e:
    print(e)

#only process data if it was retreived correctly
if 'data' in data.keys():
    
    #create two lists of time and tide height
    time_list = [] #independent variable
    tide_height_list = [] #dependent variable

    max = -10
    min = 15

    for row in data["data"]: 
        
        #search for max in min inside data
        tide_height = float(row['v'])
        if(tide_height < min):
            min = tide_height
        elif(tide_height > max):
            max = tide_height

        tide_height_list.append(tide_height)
        time_list.append(dt.datetime.strptime(row['t'], '%Y-%m-%d %H:%M'))

    end_date = start_date + dt.timedelta(days=14)
    
    #Build the title for the graph
    title = "Tide Heights: Station 8454000 ("
    title += start_date.date().strftime("%Y-%m-%d") + " to "
    title += end_date.date().strftime("%Y-%m-%d") + ")"
   
   

   
    #set up the graph to be generated
    axes = plt.axes()
    axes.set_title(title)
    axes.set_ylabel("Tide Height (meters)")
    axes.set_xlabel("Date")
    axes.set_ylim([-0.5, 2.0])
    axes.set_xlim([start_date, end_date])
    axes.set_yticks([ -0.5, 0, 0.5, 1.0, 1.5, 2.0])
    plt.plot(time_list, tide_height_list)
    plt.text(start_date + dt.timedelta(hours=12), 1.75, f"Max: {max}\nMin: {min}", bbox=dict(facecolor='blue', alpha=0.5))
    plt.show()