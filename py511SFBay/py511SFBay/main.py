import sys
import argparse
from datetime import datetime
import py511SFBay
from py511SFBay.api import RTD
from py511SFBAY.utils import Window

#This needs a lot of work because it is different from bart

# Initialize RTD API
rtd = RTD(settings.RTD_API_KEY or settings.DEFAULT_API_KEY)

AGENCIES = rtd.get_agencies()


# Parse command line arguments
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--version', action='version', version=py511SFBay.__version__)
    parser.add_argument('-a','--agency', nargs='?', help='511 transit agencies, defaults to caltrain', choices=AGENCIES.keys(), default='Caltrain')
    parser.add_argument('-rn','--route', nargs='?', help='routes name')
    parser.add_argument('-rc','--routecode', nargs='?', help='routes code')
    parser.add_argument('-sn','--station', nargs='?', help='station name')
    parser.add_argument('-sc','--station', nargs='?', help='station code')
    parser.add_argument('-l','--list', action='store_true', help='list available options')

    args = parser.parse_args()
    return args

arguments = get_args()

try:
	stations = rtd.get_routes(arguments)
except RuntimeError as error:
	print(error)
	exit(1)

for station in stations:
	print('{abbr} - {name}'.format(
		abbr=station[0], name=station[1]))

		#Unrecognized option
	# else:
	# 	print(
	# 		'RealTimeDeparture: Unrecognized option \'{option}\'\n'
	# 		'Try \'rtd --help\'for more information.'.format(
	# 			option=argument))
	# 	exit(1)
	exit()


# Use the default stations unless ones were specified
try:
	arguments = arguments or settings.RTD_STATIONS.split(',')
except AttributeError:
	pass

# Show the usage text if no stations were specified
if not arguments:
	print(settings.USAGE_TEXT)
	exit(1)


def draw():
    """Draw the information on the terminal."""
    y = 0

    # Display the current time
    window.center(y, 'Real Time Departures as of {time}'.format(
        time=datetime.now().strftime('%I:%M:%S %p')))

    # # Display advisories (if any)
    # advisories = rtd.get_advisories()
    # for advisory in advisories:
    #     window.clear_lines(y + 1)
    #     y += 2
    #     window.addstr(y, 0, '{type} ({posted}) - {sms_text}'.format(
    #         posted=advisory.posted,
    #         type=advisory.type,
    #         sms_text=advisory.sms_text,
    #     ), color_name='RED', bold=True)

    # Display stations
    for station_abbr in arguments:
        window.clear_lines(y + 1)
        y += 2
        station, departures = rtd.get_departures(station_abbr)
        window.addstr(y, 0, station, bold=True)

        # Display all destinations for a station
        for destination, estimates in departures:
            y += 1
            window.addstr(y, 0, destination + ' ' * (
                window.spacing - len(destination)))
            x = window.spacing

            # Display all estimates for a destination on the same line
            for i, estimate in enumerate(estimates, start=1):
                window.addstr(y, x, '# ', color_name=estimate.color)
                x += 2

                minutes = estimate.minutes + ' '
                window.addstr(y, x, minutes, bold=True)
                x += len(minutes)

                length = '({length} car)'.format(length=estimate.length)
                window.addstr(y, x, length)
                x += len(length)

                # Clear the space between estimates
                space = (i + 1) * window.spacing - x
                if space > 0:
                    window.addstr(y, x, ' ' * space)
                    x += space

            # Clear the rest of the line
            remaining = window.width - x
            if remaining > 0:
                window.addstr(y, x, ' ' * remaining)

    # Display help text at the bottom
    window.clear_lines(y + 1)
    window.addstr(y + 2, 0, 'Press \'q\' to quit.')

    # Clear the bottom 2 lines in case rows were moved up
    window.clear_lines(y + 3, lines=2)





def main():
    """Keep running until 'q' is pressed to exit or an error occurs."""
    char = ''

    while char != 'q':
        try:
            draw()
        except RuntimeWarning:
            pass
        except RuntimeError as error:
            window.endwin()
            print(error)
            exit(1)

        char = window.getch()

    window.endwin()
