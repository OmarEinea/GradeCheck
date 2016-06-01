#!/usr/bin/env python

# import needed libraries
import mechanize
from bs4 import BeautifulSoup


# A class to manage information flow
class Scrape:
    def __init__(self, exceptions):
        # Instantiate an empty browser holder
        self.br = None
        # Declare and store exception courses
        self.exceptions = exceptions
        # Store root url in shortcut variable as it's going to be use a lot
        self.root_url = "https://uos.sharjah.ac.ae:9050/prod_enUS"

    def initialize(self):
        # Instantiate mechanize browser
        self.br = mechanize.Browser()
        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Login to official UOS UDC
    def login(self, sid, pin):
        self.initialize()
        # Open original UOS UDC login url
        self.br.open(self.root_url + "/twbkwbis.P_WWWLogin")
        # Fill up login form and submit
        self.br.select_form(nr=0)
        self.br["sid"] = sid
        self.br["PIN"] = pin
        self.br.submit()

    # Returns student's Active Registrations
    def get_transcript(self):
        # Enter Student > Student Records section
        self.br.open(self.root_url + "/twbkwbis.P_GenMenu?name=bmenu.P_AdminMnu")
        # Enter Academic Transcript page
        self.br.follow_link(url="/prod_enUS/bwskotrn.P_ViewTermTran")
        # Go on and submit
        self.br.select_form(nr=1)
        self.br.submit()
        # Put page in a soup and store it in transcript
        return self.br.response().read()

    # Loop through Transcript page checking for grades
    def check_grades(self):
        # Get Transcript page and put it in a soup
        soup = BeautifulSoup(self.get_transcript(), "lxml")
        # Initialize a flag for when loop is inside needed area
        inside = False
        # Loop through all html tr tags in soup
        for tr in soup.body.find("table", class_="datadisplaytable").find_all("tr"):
            # Make sure th tag isn't None
            if tr.th is not None:
                # When it reaches "Spring 2015-2016"
                if tr.th.text == "Term: Spring 2015-2016":
                    # This is where needed area starts
                    inside = True
                # when it reaches "Term Totals"
                elif inside and tr.th.text == "Term Totals (Undergraduate)":
                    # This is where needed area ends
                    break
            # If it's inside needed area and it's a course "tr" (because of having "td")
            if inside and tr.find().name == "td":
                # Notify me if a new course grade is out :)
                self.notify_if_new_grade(tr.find_all())

    # Notify me if "td" tags contain a new grade
    def notify_if_new_grade(self, tds):
        # Loop through all exception courses
        for exception in self.exceptions:
            # Only notify if the course isn't an exception
            if exception == tds[4].text:
                return
        # Notify me that a new course Grade is out
        os.system("say '" + tds[4].text + " Grade is: " + tds[5].text + "'")
        print(tds[4].text + " Grade is: " + tds[5].text)


import os, time, random
scrape = Scrape([])

while True:
    os.system("reset")
    scrape.login("", "")
    scrape.check_grades()
    print("Last checked: " + time.strftime("%I:%M:%S"))
    time.sleep(random.uniform(900, 1800))

