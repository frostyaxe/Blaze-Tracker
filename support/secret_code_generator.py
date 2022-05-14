'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Random secret code generator.

Created on 13-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''
from . import choice, ascii_uppercase, ascii_lowercase, digits, length

def get_code():
    return ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(length))
