from bs4 import BeautifulSoup
import requests
from threading import Thread
from time import sleep
from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()

pnumber = os.environ["PHONE_NUMBER"]

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = os.environ["TWILIO_USER_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(username=account_sid, password=auth_token)

def threaded_function():
  value = True
  while (value):
    print('Scraper is running!')
    page = requests.get("https://classes.cornell.edu/browse/roster/SP23/class/CS/4820")
    soup = BeautifulSoup(page.content, "html.parser")
    section = soup.find('li', attrs={"class": "section-alt section-alt-details open-status"}).find("span")
    cStatus = section.attrs['data-content']
    
    if cStatus == 'Open' or cStatus == 'Waitlist':
      message = client.messages.create(
        body="Algo is Open",
        from_="+18777804236",
        to="+16094127767"
      )
      value = False
      break
    sleep(600)
    
 
def find_from_option(is_lec, num, season, dept, course_num):
  value = True
  while (value):
    print('Scraper is running!')
    page = requests.get(f"https://classes.cornell.edu/browse/roster/{season}/class/{dept}/{course_num}")
    soup = BeautifulSoup(page.content, "html.parser")
    if is_lec:
      section = (soup
                 .find('ul', attrs={"aria-label": f"Class Section LEC {num}"})
                 .find('li', attrs={"class": "section-alt section-alt-details open-status"})
                 .find("span"))
    else:
      section = (soup
                 .find('ul', attrs={"aria-label": f"Class Section DIS {num}"})
                 .find('li', attrs={"class": "section-alt section-alt-details open-status"})
                 .find("span"))
      
    
    cStatus = section.attrs['data-content']
    
    if cStatus == 'Open' or cStatus == 'Waitlist' or cStatus == 'Closed':
      message = client.messages.create(
        body=f"{dept} {course_num} is {cStatus}",
        from_="+18777804236",
        to=f"{pnumber}"
      )
      
      print(message.sid)
      
      print("Closed")
      
      value = False
      break
    sleep(600)
 
if __name__ == "__main__":
    thread = Thread(target = lambda: find_from_option(True, '002', "SP24", "AEM", "4140"))
    thread.start()
    thread.join()
    print("thread finished...exiting")