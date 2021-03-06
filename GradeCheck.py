#!/usr/bin/env python

import time, random
from Scrape import Scrape
from Data import *

scrape = Scrape(known_courses)

while True:
    try:
        scrape.login(username, password)
        scrape.check_grades(term)
    except:
        print("Error Occurred")
    print("Last checked: " + time.strftime("%I:%M:%S"))
    time.sleep(random.uniform(500, 750))
