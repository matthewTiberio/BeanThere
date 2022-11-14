from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
import os
import argparse
import json
import pprint
import requests
import sys
import urllib

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'

API_KEY = os.environ['YELP_KEY'] 

DEFAULT_TERM = 'coffee'
DEFAULT_LOCATION = 'Toronto'
SEARCH_LIMIT = 3

# Create your views here.
def landing(request):
    return render(request, 'landing.html')

def signup (request):
  return render(request, 'registration/signup.html')

# Define the home view
def home(request):
  return render(request, 'users/home.html')

# Define the home view
def index(request):
  response_data = api_search(API_KEY, DEFAULT_TERM, DEFAULT_LOCATION)
  search_data = response_data.get('businesses')
  print(search_data)
  return render(request, 'users/index.html', 'data': search_data)

# Define the details view
def details(request):
  return render(request, 'users/details.html')

# Define the user view
def user(request):
  return render(request, 'users/user.html')

# Define the review view
def review(request):
  return render(request, 'users/review.html')


def api_search(api_key, term, location):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return api_request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def api_request(host, path, api_key, url_params=None):
  url_params = url_params or {}
  url = '{0}{1}'.format(host, quote(path.encode('utf8')))
  headers = {
    'Authorization': 'Bearer %s' % api_key,
  }

  print(u'Querying {0} ...'.format(url))

  response = requests.request('GET', url, headers=headers, params=url_params)

  return response.json()