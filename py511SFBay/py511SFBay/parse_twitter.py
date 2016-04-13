
# Parse the twitters for updates about the transit option you chose


## doing this here, but it should be moved

class Station(object):
	def __init__(self, agency, name=None, code=None):
		self.agency = agency
		self.name = name
		self.code = code
		self.departures = []
		self.url = ""

	def add_departure(self, departure):
		if not isinstance(departure, Departure):
			raise TypeError("Must be an object of type Departure")
		self.departures.append(departure)

	def list_departures(self):
		for departure in self.departures:
			print departure.time

	def list_routes(self):
		for departure in self.departures:
			print departure.route

	def list_directions(self):
		for departure in self.departures:
			print departure.direction

	def get_directions(self):
		return set(i.direction for i in self.departures)

	def get_routes(self):
		return set(i.route for i in self.departures)

	def get_departures_from_direction(self, input_direction):
		return [i for i in self.departures if i.direction == input_direction]

	def order_departures(self):
		self.departures = sorted(self.departures, key=lambda departure: departure.time)
		self.departures = sorted(self.departures, key=lambda departure: departure.direction)




class Departure(object):
	def __init__(self, route, direction, time):
		self.route = route
		self.direction = direction
		self.time = int(time)