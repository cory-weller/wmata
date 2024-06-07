#!/usr/bin/env python3

import sys, http.client, urllib.request, urllib.parse, urllib.error, base64, xmltodict, json
from time import sleep

args = sys.argv[1:]

starting_station = ' '.join(args)

if starting_station == '':
    exit('provide exactly 1 argument (starting station)!')

with open('wmata-token.txt', 'r') as infile:
    wmata_api_token = infile.read().strip()

def get_params(from_station_code, to_station_code):
    params = urllib.parse.urlencode({
        # Request parameters
        'FromStationCode': from_station_code,
        'ToStationCode': to_station_code,
    })
    return params

def read_station_station_output(my_json):
    tripinfo = json.loads(my_json)
    tripinfo = tripinfo['StationToStationInfos'][0]
    station1 = station_names[tripinfo['SourceStation']]
    station2 = station_names[tripinfo['DestinationStation']]
    fare = tripinfo['RailFare']['PeakTime']
    distance = tripinfo['CompositeMiles']
    return((station1, station2, distance, fare))

# Get all station info
with open('stations.xml', 'r') as infile:
    xml_data = infile.read()

stations = xmltodict.parse(xml_data)['StationsResp']['Stations']['Station']

def sanitize(name):
    name = name.replace('/', '-')
    name = name.replace("'", '')
    name = name.replace(' ', '-')
    return(name)

start_station_filename = sanitize(starting_station) + '.tsv'

# Build dictionary for station name : code
station_codes = {}
for station in stations:
    name = station['Name']
    code = station['Code']
    station_codes[name] = code

station_names = list(station_codes.keys())

if starting_station not in station_names:
    print('ERROR: Starting station not in list of station names!')
    print('Valid station names include the following:')
    print('\n'.join(station_names))
    exit()

# Build reverse lookup dictionary for station code : name
station_names = {v: k for k, v in station_codes.items()}



headers = {
    # Request headers
    'api_key': wmata_api_token,
}



# Ensure starting station is valid name
destinations = list(station_codes.values())

out_table = []

station1_code = station_codes[starting_station]
# Collect station-to-station information
station_station_data = []
for destination in destinations:
    sleep(0.5)
    if station1_code == destination:
        continue
    params = get_params(station1_code, destination)
    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Rail.svc/json/jSrcStationToDstStationInfo?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        data = data.decode()
        station_station_data.append(data)
        info = read_station_station_output(data)
        out_table.append(info)
        #print( )
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


output_header = 'Start\tDestination\tDistance_mi\tFare_USD\n'
with open(start_station_filename, 'w') as outfile:
    outfile.write(output_header)
    for info_line in out_table:
        start, dest, dist, fare = info_line
        outfile.write(f'{start}\t{dest}\t{dist:.2f}\t{fare:.2f}\n')
