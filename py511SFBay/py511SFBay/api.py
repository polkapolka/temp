try:
    import requests
except ImportError:
    import requests

import re
import errno
import json
import xml.etree.ElementTree as ET
import pdb

class RTD(object):
    """Wrapper for the 511 RTD api."""

    BASE_URL = 'http://services.my511.org/Transit2.0'
    AGENCY_URL = 'GetAgencies.aspx'
    ROUTES_4_AGENCIES_URL = 'GetRoutesForAgencies.aspx'
    ROUTES_4_AGENCY_URL = 'GetRoutesForAgency.aspx'
    STOPS_4_ROUTE_URL = 'GetStopsForRoute.aspx'
    STOPS_4_ROUTES_URL = 'GetStopsForRoutes.aspx'
    DEPART_4_STOPNAME_URL = 'GetNextDeparturesByStopName.aspx'
    DEPART_4_STOPCODE_URL = 'GetNextDeparturesByStopCode.aspx'
    API_KEY = ''
    ADVISORY_URL = ''
    DEPARTURE_URL = ''
    STATION_URL = ''
    invalid_names = {'GREAT MALL/MAIN TRANSIT CTR-S MAIN ST & GREAT MALL PKWY':'GREAT MALL/MAIN TRANSIT CTR-S MAIN ST'}

    def __init__(self, key):
        """ Set the API key."""
        self.API_KEY = key

    def _build_url(self, endpoint, **kwargs):
        query_string = {'token':self.API_KEY}
        if kwargs:
            query_string.update(kwargs)
        return '{}/{}?'.format(self.BASE_URL, endpoint), query_string

    def _get_XML_root(self, endpoint, **kwargs):
        """ Get the XML root of the response from the specified URL. """
        url, query_string = self._build_url(endpoint, **kwargs)
        try:
            response = requests.get(url, params=query_string)
        except requests.exceptions.ConnectionError as error:
            raise RuntimeError('Connection Failed.')
        return response.text        

    def _get_content(self, endpoint, **kwargs):
        """ Converts XML result to an ElementTree object. Checks for API Error.  """
        r = self._get_XML_root(endpoint, **kwargs)
        root = ET.fromstring(r)
        if re.search("Error|error", root.tag):
            raise Exception(root.tag, root.text)
        else:
            return root

    def get_agencies(self):
        """ Returns a dictionary of the agencies served by 511
        and the mode of transportation. """
        root = self._get_content(self.AGENCY_URL)
        return self._parse_ET(root,"Agency",'Name','Mode')


    def get_routes(self, agency):
        """ Returns the routes for an Agency."""
        #pdb.set_trace()
        root = self._get_content(self.ROUTES_4_AGENCY_URL, agencyName=agency)
        routes = {}
        for child in root.iter(tag="Route"):
            routeinfo = {}
            routeinfo['Code']=child.attrib['Code']
            routeinfo['Direction'] = self._parse_ET(child, 'RouteDirection', 'Name', 'Code')
            routes[child.attrib['Name']] = routeinfo
        return routes

    def get_stations(self, agency,route, routeDirection=None):
        """ Returns the stations for a Route and a routeDirection."""
        #pdb.set_trace()
        IDFname = '{}~{}~{}'.format(agency,route,routeDirection)
        if agency == 'BART':
            IDFname = '{}~{}'.format(agency,route)
        root = self._get_content(self.STOPS_4_ROUTE_URL, routeIDF=IDFname)
        return self._parse_ET(root,'Stop','name','StopCode')

    def get_departures(self, agency, stationName=None, stationCode=None):
        """ Returns the departure times for a station. """
        #pdb.set_trace()
        if stationName is not None and stationCode is not None:
            raise Exception('Use only StationName or StationCode.')
        elif stationName:
            url = self.DEPART_4_STOPNAME_URL
            #return self._get_stationName_departures(agency, stationName)
        elif stationCode:
            url = self.DEPART_4_STOPCODE_URL
            #return self._get_stationCode_departures(agency, stationCode)
        else:
            raise Exception("StationName or StationCode not present.")
        root = self._get_content(url, agencyName = agency, stationName=stationName, StopCode=stationCode)
        newtag = "RouteDirection"
        if agency == 'BART':
            newtag = "Route"
        departures = {}
        for child in root.iter(tag="Route"):
            departures[child.attrib['Name']] = self._get_times(child, newtag)
        stationinfo = {}
        stationinfo['routes']= departures
        for child in root.iter(tag="Stop"):
            stationinfo['name'] = child.attrib['name']
            stationinfo['code'] = child.attrib['StopCode']
        return stationinfo

    def get_advisories(self):
        """ Get the current service advisories."""
        root = self._get_xml_root(self.ADVISORY_URL)
        advisories = []
        for advisory in root:
            # Ignore advisories that stat there aren't any delays
            try:
                advisories.append(advisory)
            except AttributeError:
                break
        return advisories
        
    def _valid_names(self, name):
        ''' Some names contain | and & characters which result in invalid parameters error from api. Those same names work if you only use the part in front of the symbol.'''
        if name in invalid_names:
            return invalid_names[name]
        else:
            return name

    def _parse_ET(self, tree, tag, keyname, valuename):
        #pdb.set_trace()
        out_dict ={}
        for branch in tree.iter(tag=tag):
            out_dict[branch.attrib[keyname]] = branch.attrib[valuename]
        return out_dict

    def _listparse_ET(self, tree, tag):
        #pdb.set_trace()
        out_list =[]
        for branch in tree.iter(tag=tag):
            out_list.append(branch.text)
        return out_list

    def _get_times(self, tree, tag):
        #pdb.set_trace()
        out_dict = {}
        for branch in tree.iter(tag=tag):
            out_dict[branch.attrib['Name']] = self._listparse_ET(branch, "DepartureTime")
        return out_dict


    # def get_departures(self, station_abbr):
    #     """ Get the current departure estimates for a station."""
    #     return (station_name, departures)

    # def get_stations(self):
    #     """ Get the abbreviations and names for all stations."""
    #     root = self._get_xml_root(self.STATION_URL)
    #     stations = []
    #     return stations
