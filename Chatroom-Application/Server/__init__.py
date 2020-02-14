from flask import Flask
from config import config

app=Flask(__name__)
app.config.from_object(config)

# Import necessary files below.

#from server import core_routes
#from server import utility_routes
#from server import helpers
