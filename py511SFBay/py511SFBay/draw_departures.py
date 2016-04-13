from datetime import datetime
from utils import Window
import settings
import pdb


def start_other_stuff(stations):
    # Initialize window
    window = Window(settings.REFRESH_INTERVAL, settings.TOTAL_COLUMNS)
    def draw(stations):
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
        y = 0
        # Display the current time
        # pdb.set_trace()
        window.center(y, 'RTD departures as of {time}'.format(
            time=datetime.now().strftime('%I:%M:%S %p')))
        stations = sorted(stations, key=lambda station: station.agency)
        cagency=""
        for station in stations:
            if station.agency != cagency:
                y+=2
                window.center(y, station.agency)
                cagency = station.agency
                y+=1
            x = window.spacing
            window.addstr(y,0,station.name)
            y+=1
            for direction in station.get_directions():
                #y+=1
                window.addstr(y,0, direction.title())
                dep_list = station.get_departures_from_direction(direction)
                for i, departure in enumerate(dep_list):
                    color = get_minutes_color(str(departure.time))
                    #pdb.set_trace()
                    window.addstr(y,(1+i%3)*x, str(departure.time) + "("+departure.route+")", color_name=color)
                    if i%3==2 and i+1 < len(dep_list):
                        #pdb.set_trace()
                        y+=1
                y+=1

        # Display help text at the bottom
        window.clear_lines(y + 1)
        x = 0
        window.addstr(y + 2, x, 'Press \'q\' to quit.')

        # Clear the bottom 2 lines in case rows were moved up
        window.clear_lines(y + 3, lines=2)

    #function
    char = ''
    while char!='q':
        try:
            draw(stations)
        except RuntimeWarning:
            pass
        except RuntimeError as error:
            window.endwin()
            print(error)
            exit(1)

        char = window.getch()
    window.endwin()



def start_stuff(departures):
    # Initialize window
    window = Window(settings.REFRESH_INTERVAL, settings.TOTAL_COLUMNS)
    def draw(things):
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
        y = 0
        # Display the current time
        #pdb.set_trace()
        window.center(y, 'RTD departures as of {time}'.format(
            time=datetime.now().strftime('%I:%M:%S %p')))
        for thing in things:
            #y+=2
            x = window.spacing
            #window.addstr(y,0,thing)
            for item in things[thing]:
                y+=2
                window.addstr(y,0, item)
                for i, dtime in enumerate(things[thing][item]):
                    color = get_minutes_color(dtime)
                    window.addstr(y,(1+i)*x, dtime + "("+thing+")", color_name=color)
                y+=1

        # Display help text at the bottom
        window.clear_lines(y + 1)
        x = 0
        window.addstr(y + 2, x, 'Press \'q\' to quit.')

        # Clear the bottom 2 lines in case rows were moved up
        window.clear_lines(y + 3, lines=2)

    #function
    char = ''
    while char!='q':
        try:
            draw(departures)
        except RuntimeWarning:
            pass
        except RuntimeError as error:
            window.endwin()
            print(error)
            exit(1)

        char = window.getch()
    window.endwin()

