from functools import wraps

from flask import session, redirect
from jenkins import Jenkins
from jwt import encode, decode

from manager.vars_manager import BlazeUrls


