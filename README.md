# README
I was annoyed at the WMATA fare lookup format so I made this to
calculate station-to-station fares for all pairs and output a
single table.

# Output


# How to use
Making calls to the WMATA API requires a developer token.
Sign up [here](https://developer.wmata.com/) and save the token to a text file named `wmata-token.txt` as it's used by `curl` and by the `python` script.

First we need to retrieve all station ID information in `xml` format to
get the alphanumeric station codes used for API calls.
```bash
wmatatoken=$(cat wmata-token.txt)
curl -v -X GET "https://api.wmata.com/Rail.svc/Stations?" \
    -H "api_key:${wmatatoken}" \
    > stations.xml
```

Then we can use [`get-trip-info.py`](get-trip-info.py) to query for
a specific station station. The script will return fare and distance
when traveling from your starting station to all possible destinations.

The name of the starting station must match the exact spelling as
indicated in [`station-names.txt`](station-names.txt).

API calls are intentionally slowed to avoid caps implemented by WMATA.

```bash
# Get info for a single station
python3 get-trip-info.py 'North Bethesda' > north-bethesda.tsv &

# Get info for all stations (will take a while)
readarray -t station_names < station-names.txt
for station in ${station_names[@]}; do
    python3 get-trip-info.py $station
done > all-station-info.tsv
```


