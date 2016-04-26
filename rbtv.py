#!/bin/python3
# Copyright 2016, Freiburg,
# Author: Markus Frey.

import sys, errno, math, argparse, datetime, requests
from lxml import html
from enum import Enum

# Terminal escape codes used for output text formatting.
class Colors:
  Bold = "\033[1m"
  Light = "\033[0;37m"
  Reset = "\033[0m"
  def disable():
    Colors.Bold = Colors.Light = Colors.Reset = ""

# Data class holding a show's information.
class Show:
  def __init__(self, time, title, details, duration):
    self.time = time
    self.title = title
    self.details = details
    self.duration = duration
    # A show's schedule position relative to the currently playing show.
    # (0: Currently playing, -n: already over n shows ago, n: n shows to go)
    self.state = None  
  # Pretty print.
  def __str__(self):
    ret = ""
    if self.state < 0:
      ret += Colors.Light
    elif self.state == 0:
      ret += Colors.Bold

    ret += self.time.strftime("%H:%M") + " " + self.title
    if self.details != "":
      ret += " " + Colors.Light + self.details
    #ret += Colors.Light + " (" + self.duration + ")"
    if self.state > 0:
      now = datetime.datetime.today()
      ret += " (in " + str(math.ceil((self.time - now).seconds / 60)) + 
        " Minuten)"
    ret += Colors.Reset
    return ret

# Construct a list of shows by scraping the webpage.
def getShowsFromWebsite():
  # Checks if the path is available and if so returns a string.
  def scrape(page, path):
    result = page.xpath(path)
    return result[0].strip() if result else ""
  # Generator iterating over an element and its direct neighbors.
  def neighborhood(iterable):
    iterator = iter(iterable)
    prev = None
    item = iterator.__next__()
    for next in iterator:
      yield(prev, item, next)
      prev = item
      item = next
    yield(prev, item, None)

  # Get webpage content.
  page = requests.get('http://www.rocketbeans.tv/wochenplan/')
  tree = html.fromstring(page.content)

  # Scrape for all shows giving them absolute datetime objects.
  result = list()
  # Find all divs with class tag 'day'.
  for day in tree.xpath(
      '//div[contains(concat(" ", normalize-space(@class), " "), " day ")]'):
    # Get the proccessed contents of the date header div.
    date = scrape(day, 'div[@class="dateHeader"]/span/text()')
    # Loop over all shows for the current weekday.
    for show in day.xpath('descendant::div[@id="show-"]'):
      time = datetime.datetime.strptime(date + " " + 
          scrape(show, 'span[@class="scheduleTime"]/text()'), 
          "%d. %b %Y %H:%M")
      title = scrape(show, 'div[@class="showDetails"]/h4/text()')
      details = scrape(show, 
          'div[@class="showDetails"]/span[@class="game"]/text()')
      duration = scrape(show, 
          'descendant::span[@class="showDuration"]/text()')
      result.append(Show(time, title, details, duration))

  # Set the shows' positions in the timeline (past, current, coming-up).
  now = datetime.datetime.today()
  for prev, current, next in neighborhood(result):
    if current.time <= now and (next == None or next.time > now):
      current.state = 0
    elif current.time > now:
      current.state = prev.state + 1
  for prev, current, next in neighborhood(result):
    if current.state != None:
      break
    if prev == None:
      current.state = - (len(result) - result[-1].state - 1)
    else:
      current.state = prev.state + 1

  return result

if __name__ == "__main__":
  # Commandline options.
  parser = argparse.ArgumentParser(
          description = "A commandline broadcasting schedule for "
            "https://www.twitch.tv/rocketbeanstv")
  parser.add_argument(
          '-c', '--no-color', 
          dest = 'noColor', 
          default = False, 
          action = "store_true", 
          help = "disable text formatting"
        )
  parser.add_argument(
          '-p', 
          dest = 'nrOfPastShows', 
          default = 1, 
          type = int, 
          help= "set the number of past shows to list (default: 1)"
        )
  parser.add_argument(
          '-f', 
          dest = 'nrOfFutureShows', 
          default = 6, 
          type = int, 
          help = "set the number of future shows to list (default: 6)"
        )
  options = parser.parse_args()

  if options.noColor:
    Colors.disable()

  try:
    for show in getShowsFromWebsite():
      if show.state < -options.nrOfPastShows:
        continue
      elif show.state > options.nrOfFutureShows:
        break
      print(show)
  except requests.exceptions.RequestException:
    print("Couldn't get the webpage.")
    sys.exit(errno.EIO)
  sys.exit(0)
