#!/usr/bin/env python

# import needed libraries
import mechanize, os, time, random
from bs4 import BeautifulSoup


# A class to manage information flow
class Scrape:
    def __init__(self):
        # Instantiate an empty browser holder
        self.br = None
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
    def grab_active_regs(self):
        # Enter Student > Registration section
        self.br.open(self.root_url + "/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu")
        # Enter Active Registration page
        self.br.follow_link(url="/prod_enUS/bwsksreg.p_active_regs")
        # Return raw html
        return self.br.response().read()

    # Notify me whether course mark are out or not
    def notify_me(self, course):
        # If course is still in the Active Registrations
        if BeautifulSoup(self.grab_active_regs(), "lxml").body.find(text=course) is None:
            # Notify me that course marks are out
            os.system("spd-say \"" + course.split(" - ")[0] + " Marks Are Out!\"")
            print(course.split(" - ")[0] + " Marks Are Out!")
        else:
            print("Last checked: " + time.strftime("%I:%M:%S"))


scrape = Scrape()

scrape.login("", "")

while True:
    scrape.notify_me("")
    time.sleep(random.uniform(900, 1800))
    os.system("reset")

