#!/usr/bin/env python
from __future__ import print_function

import argparse
import collections
import gzip
import json
import sys
import warnings


from resolver import get_resolver
from location import Location, LocationEncoder
import os

def parse_args():
    parser = argparse.ArgumentParser(
        description='Resolve tweet locations.',
        epilog='Paths ending in ".gz" are treated as gzipped files.')
    parser.add_argument('-s', '--statistics',
        action='store_true',
        help='show summary statistics')
    parser.add_argument('--order',
        metavar='RESOLVERS',
        help='preferred resolver order (comma-separated)')
    parser.add_argument('--options',
        default='{}',
        help='JSON dictionary of resolver options')
    parser.add_argument('--locations',
        metavar='PATH', dest='location_file',
        help='path to alternative location database')
    parser.add_argument('input_file', metavar='input_path',
        nargs='?', default=sys.stdin,
        help='file containing tweets to locate with geolocation field '
             '(defaults to standard input)')
    parser.add_argument('output_file', metavar='output_path',
        nargs='?', default=sys.stdout,
        help='file to write geolocated tweets to (defaults to standard '
             'output)')
    return parser.parse_args()


def open_file(filename, mode):
    if filename.endswith('.gz'):
        return gzip.open(filename, mode)
    else:
        return open(filename, mode)


def main(tweet):
    resolver_kwargs = {}

    resolver = get_resolver(**resolver_kwargs)
    
    resolver.load_locations(location_file=None)
    # Variables for statistics.
    city_found = county_found = state_found = country_found = 0
    has_place = has_coordinates = has_geo = has_profile_location = 0
    resolution_method_counts = collections.defaultdict(int)
    skipped_tweets = resolved_tweets = total_tweets = 0
    # Collect statistics on the tweet.
    if tweet.get('place'):
        has_place += 1
    if tweet.get('coordinates'):
        has_coordinates += 1
    if tweet.get('geo'):
        has_geo += 1
    if tweet.get('user', {}).get('location', ''):
        has_profile_location += 1
    # Perform the actual resolution.
    resolution = resolver.resolve_tweet(tweet)
    if resolution:
        location = resolution[1]
        tweet['location'] = location
        # More statistics.
        resolution_method_counts[location.resolution_method] += 1
        if location.city:
            city_found += 1
        elif location.county:
            county_found += 1
        elif location.state:
            state_found += 1
        elif location.country:
            country_found += 1
        resolved_tweets += 1
    total_tweets += 1
    print('Resolved locations for %d of %d tweets.' % (
        resolved_tweets, total_tweets), file=sys.stderr)
    if resolved_tweets < total_tweets:
        return False, {}
    else:
        return True, tweet

if __name__ == '__main__':
    main()
