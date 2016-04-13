import argparse
import api
import logging
import settings
import sys
import draw_departures
from pprint import pprint
from datetime import datetime
#from draw_departures import start_stuff
from curses import wrapper
from parse_twitter import Station, Departure

import pdb

logging.basicConfig(filename="debug.log",level=logging.DEBUG)


logger = logging.getLogger()

rtd = api.RTD("d186b10e-694d-4ede-9689-55f36514b058")
try:
	agencies = rtd.get_agencies()
except RuntimeError as error:
	logger.critical(error)

logger.debug(agencies)

parser = argparse.ArgumentParser(description="511 RTD API")
parser.add_argument('-a', nargs='?', help='511 transit agencies', dest='agency', choices=agencies.keys())
parser.add_argument('-rn', nargs='?', help='routes name', dest='routeName')
parser.add_argument('-d', nargs='?', help='direction', dest='direction')
parser.add_argument('-sn', nargs='?', help='station name', dest='stationName')
parser.add_argument('-sc', nargs='?', help='station code', dest='stationCode')
parser.add_argument('-l', action='store_true', help='list available options', default=False, dest='list')
parser.add_argument('-m', action='store_true', help='return a departure time from stopcode or stopname', default=False, dest='mode')
parser.add_argument('-s', action='store_true', help='enter setup mode', default=False, dest='setup')
args = parser.parse_args()


def addDeparturesToStation(newStation, departures):
	#pdb.set_trace()
	for route, directions in departures.items():
		for direction, times in directions.items():
			for time in times:
				#pdb.set_trace()
				d = Departure(route, direction, time)
				newStation.add_departure(d)




#logger.debug(rtd.get_stations('Caltrain','LIMITED','NB'))

# -l enables list mode
if args.list:
	if args.direction is not None and args.routeName is not None:
		if args.agency == "BART":
			#pdb.set_trace()
			routes = rtd.get_routes(args.agency)
			stops = rtd.get_stations(args.agency, routes[args.routeName]["Code"])
		else:
			try:
				stops = rtd.get_stations(args.agency, args.routeName, args.direction)
			except RuntimeError as error:
				logger.critical(error)
			logger.debug(stops)
		print "Code".ljust(14), " - ", "Stop Name"
		for stop in stops.keys():
			sys.stdout.flush()
			print stops[stop].ljust(14)," - ",stop
	elif args.agency is not None:
		try:
			routes = rtd.get_routes(args.agency)
		except RuntimeError as error:
			logger.critical(error)
		logger.debug(routes)
		if agencies[args.agency]:
			print "Route".ljust(30)," - ", "Directions"
			for route in routes.keys():
				sys.stdout.flush()
				if args.agency != "BART":
					print route.ljust(30)," - ",routes[route]['Direction'].values()
				elif args.agency == "BART":
					'''BART only has Routes with no direction.  The route is the direction.'''
					print route.ljust(30), " - ", route
	else:
		#pdb.set_trace()
		print "Agency - Type"
		for agency, mode in agencies.items():
			print "%s - %s" % (agency, mode)
		#pdb.set_trace()

# need a function to get station name from station code and vice versa
# -m enables departure mode
elif args.mode:
	#pdb.set_trace()
	if args.agency is not None and args.stationCode is not None:
		try:
			departures = rtd.get_departures(args.agency, stationCode=args.stationCode)
			newStation = Station(args.agency, code=departures['code'], name=departures['name'])
			addDeparturesToStation(newStation, departures['routes'])
			#wrapper(start_stuff)
			newStation.order_departures()
			#pdb.set_trace()
			draw_departures.start_other_stuff([newStation])
			#draw_departures.start_stuff(departures)
		except RuntimeError as error:
			logger.critical(error)
		logger.debug(departures)
		pprint(departures)
	elif args.agency is not None and args.stationName is not None:
		try:
			departures = rtd.get_departures(args.agency, stationName=args.stationName)
			#wrapper(start_stuff)
			#draw_departures.start_stuff(departures)
		except RuntimeError as error:
			logger.critical(error)
		logger.debug(departures)
		pprint(departures)
	else:
		print "Station Name or Station Code needed to return departure times.\n  Try list mode \'-l\' to find the right Station info."


# -s enables setup mode
# setup mode creates a list of home stations and a list of work stations
# these can be called by simply using rtd home or rtd work
# 


# # Initialize window
# window = Window(settings.REFRESH_INTERVAL, settings.TOTAL_COLUMNS)


# def draw():
#     """Draw the information on the terminal."""
#     y = 0

#     # Display the current time
#     window.center(y, 'Real Time Departures Setup')
#     window.addstr(y+2,0,'Press 1 to create HOME_LIST')
#     window.addstr(y+4,0,'Press 2 to create WORK_LIST')
#     # window.center(y, 'Real Time Departures as of {time}'.format(
#     #     time=datetime.now().strftime('%I:%M:%S %p')))

#     # Display help text at the bottom
#     window.clear_lines(y + 1)
#     window.clear_lines(y + 3)
#     window.addstr(y + 7, 0, 'Press \'q\' to quit.')

#     # Clear the bottom 2 lines in case rows were moved up
#     window.clear_lines(y + 5, lines=2)


# if args.setup:
#     char = ''

#     while char != 'q':
#         try:
#             draw()
#         except RuntimeWarning:
#             pass
#         except RuntimeError as error:
#             window.endwin()
#             print(error)
#             exit(1)

#         char = window.getch()

#     window.endwin()