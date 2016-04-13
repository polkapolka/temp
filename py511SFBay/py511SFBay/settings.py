import os

# Everything is cool here except the example
USAGE_TEXT = (
    'Usage: rtd [OPTION]... [STN]...\n'
    'Display real time estimates about the STNs\n'
    '(using the RTD_STATIONS environment variable if not specified).\n\n'
    'Options\n'
    '  -l, --list     print list of station abbreviations and exit\n'
    '  -h, --help     display this help and exit\n'
    '  -v, --version  output version information and exit\n\n'
    'Examples\n'
    '  rtd mcar       get estimates for the MacArthur station\n'
    '  rtd embr cols  get estimates for the Embarcadero and Coliseum stations'
	)

DEFAULT_API_KEY = "d186b10e-694d-4ede-9689-55f36514b058"

#Who knows if this is okay right now... bah
REFRESH_INTERVAL = 100  # Milliseconds
TOTAL_COLUMNS = 4

# This doesn't exist, but the Default does exist
RTD_API_KEY = os.environ.get('RTD_API_KEY')

### This csv with stations doesn't exist... and the default doesn't exist
RTD_STATIONS = os.environ.get('RTD_STATIONS')