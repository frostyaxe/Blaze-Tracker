'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
@summary: Provides the helper functions for handling the password encoding and decoding.

Created on 03-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''

from . import wraps
from . import session
from . import encode
from . import decode
from . import redirect
from . import BlazeUrls
    
def auth_required(func):
    @wraps(func)
    def wrapper(obj,*args, **kwargs):
        if "authenticated" not in session or not session["authenticated"]:
            return redirect(BlazeUrls.ADMIN_LOGIN)
        return func(obj,*args, **kwargs)
    return wrapper

def api_auth_required(func):
    @wraps(func)
    def wrapper(obj,*args, **kwargs):
        from flask import request
        token = request.args.get('token')
        if not token:
            return {"status":"error", "message":"Missing Blaze Token!"}, 401
        try:
            decode_password(token)
        except:
            return {"status":"error", "message":"Invalid Blaze Token!"}, 401
        return func(obj,*args, **kwargs)
    return wrapper
    
def encode_password(secret):
    from config import BLAZE
    return encode({"secret": secret}, BLAZE["AUTH"]["SECRET_KEY"], algorithm=BLAZE["AUTH"]["ALGORITHM"])


def decode_password(encoded_string):
    from config import BLAZE
    return decode(encoded_string, BLAZE["AUTH"]["SECRET_KEY"], algorithms=[BLAZE["AUTH"]["ALGORITHM"]])

