# All Fares Table

See [here](all-trips.tsv).


# Why?
I was annoyed at the WMATA fare lookup format so I made this to
calculate fares for all combinations between a starting station and all other stations.

# How do?
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

Individual station file names are in the format of `<starting station>.tsv`, with spaces or `/` characters replaced with `-`. For example, running the script with `'Woodley Park-Zoo/Adams Morgan'` saves `Woodley-Park-Zoo-Adams-Morgan.tsv`

```bash
# Get info for a single station
python3 get-trip-info.py Metro Center
python3 get-trip-info.py "L'Enfant Plaza"   # Note quote requirement
python3 get-trip-info.py North Bethesda
python3 get-trip-info.py King St-Old Town

# Get all stations (will be a while...)
bash get-all-trips.sh && 
```

