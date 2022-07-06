import os
import re

from neomodel import config

from web.graph_database.models.system import System
from web.graph_database.models.person import Person

NEO4J_AUTH = re.findall('^(.*?)/(.*)$', os.environ.get('NEO4J_AUTH'))[0]
NEO4J_HOST = os.environ.get('NEO4J_HOST')
NEO4J_PORT = os.environ.get('NEO4J_PORT')

config.DATABASE_URL = f'bolt://{NEO4J_AUTH[0]}:{NEO4J_AUTH[1]}@{NEO4J_HOST}:{NEO4J_PORT}'  
