from datetime import datetime
from utils import Window
import settings

def start_stuff():
    

        try:
            new_draw(kwargs)
        except RuntimeWarning:
            pass
        except RuntimeError as error:
            window.endwin()

        



def draw_departures(stationNames, departures):
    """Draw the information on the terminal."""
    char = ''

    while char != 'q':
        y = 0
        # Display the current time
        window.center(y, 'RTD departures as of {time}'.format(
            time=datetime.now().strftime('%I:%M:%S %p')))

        # Display stations
        for stationName in stationNames:
        	window.addstr(y, 0, stationName, bold=True)
            for routes in departures:
                window.clear_lines(y + 1)
                y += 2
                window.addstr(y,0, routes)
                # Display all destinations for a station
                for element in departures:
                    y += 1
                    window.addstr(y, 0, element)
                # for destination, estimates in departures:
                #     y += 1
                #     window.addstr(y, 0, destination + ' ' * (
                #         window.spacing - len(destination)))
                #     x = window.spacing

                #     # Display all estimates for a destination on the same line
                #     for i, estimate in enumerate(estimates, start=1):
                #         window.addstr(y, x, '# ', color_name=estimate.color)
                #         x += 2

                #         minutes = estimate.minutes + ' '
                #         color = get_minutes_color(estimate.minutes)
                #         window.addstr(y, x, minutes, color_name=color, bold=True)
                #         x += len(minutes)

                #         length = '({length} car)'.format(length=estimate.length)
                #         color = get_length_color(estimate.length)
                #         window.addstr(y, x, length, color_name=color)
                #         x += len(length)

                #         # Clear the space between estimates
                #         space = (i + 1) * window.spacing - x
                #         if space > 0:
                #             window.addstr(y, x, ' ' * space)
                #             x += space

                #     # Clear the rest of the line
                #     remaining = window.width - x
                #     if remaining > 0:
                #         window.addstr(y, x, ' ' * remaining)

            # Display help text at the bottom
            window.clear_lines(y + 1)
            window.addstr(y + 2, 0, 'Press \'q\' to quit.')
        char = window.getch()
    window.endwin()


def get_minutes_color(minutes):
    """Get the color to use for the minutes estimate."""
    try:
        minutes = int(minutes.split()[0])
        if minutes <= 5:
            return 'RED'
        elif minutes <= 10:
            return 'YELLOW'
    except ValueError:
        return 'RED'




def draw():
    # Initialize window
    window = Window(settings.REFRESH_INTERVAL, settings.TOTAL_COLUMNS)
    """Draw the information on the terminal."""
    y = 0

    # Display the current time
    window.center(y, 'Real Time Departures Setup')
    window.addstr(y+2,0,'Press 1 to create HOME_LIST')
    window.addstr(y+4,0,'Press 2 to create WORK_LIST')
    # window.center(y, 'Real Time Departures as of {time}'.format(
    #     time=datetime.now().strftime('%I:%M:%S %p')))

    # Display help text at the bottom
    window.clear_lines(y + 1)
    window.clear_lines(y + 3)
    window.addstr(y + 7, 0, 'Press \'q\' to quit.')

    # Clear the bottom 2 lines in case rows were moved up
    window.clear_lines(y + 5, lines=2)