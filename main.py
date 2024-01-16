import dataclasses
import requests
import json
import pytz
from datetime import datetime


   
@dataclasses.dataclass 
class DateTime:
    year: int
    month: int
    day: int
    hour: int = 0
    minute: int = 0
    
    @staticmethod
    def fromisoformat(iso_str):
        # Split the date and time parts
        dt = datetime.fromisoformat(iso_str)


        return DateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

        

    
    
@dataclasses.dataclass
class Event:
    name: str
    start_datetime: DateTime  
    end_datetime: DateTime
    
    
     

 
def getCalendar(date_from, date_to):    
    response = requests.get(f"https://www.googleapis.com/calendar/v3/calendars/spsacademiccal%40gmail.com/events?key=AIzaSyBxoBIAkPxbC1hZNtFOmpHFv_z2ya9I838&timeMin={date_from.year}-{date_from.month}-{date_from.day}T00%3A00%3A00-05%3A00&timeMax={date_to.year}-{date_to.month}-{date_to.day}T00%3A00%3A00-05%3A00&singleEvents=true&maxResults=9999", {"fmt": "json"})
    if response.status_code == 200:
        calander_events = []
        for item in response.json()["items"]:
            
            if item["status"] == "confirmed":
                try:
                    name = item["summary"]
                    start_datetime = DateTime.fromisoformat(item["start"]["dateTime"])
                    end_datetime = DateTime.fromisoformat(item["end"]["dateTime"])
                    calander_events.append(Event(name, start_datetime, end_datetime))
                except:
                    continue
                
        return calander_events
    else:
        print(f"Failed to retrieve calander {response.status_code}")
        return None

def downloadCalendar(calander_events, file_name):
    with open(file_name, 'w') as file:
        json_data = [dataclasses.asdict(event) for event in calander_events]
        json.dump(json_data, file, indent=4)

calander_events = getCalendar(DateTime(2024, 1, 15), DateTime(2024, 4, 1)) 
downloadCalendar(calander_events, "calendar.json")