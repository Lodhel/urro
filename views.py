import json

import requests
from aiohttp import web
from aiohttp.web_response import json_response
from aiohttp_cors import CorsViewMixin
from tablib import Dataset

from models import DebtorCard


routes = web.RouteTableDef()

