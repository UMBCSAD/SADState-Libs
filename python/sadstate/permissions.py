from enum import Flag
from functools import reduce

#https://stackoverflow.com/a/42253518
def _flag_all(cls:type[Flag])->Flag:
    return cls(reduce(lambda a,b: a|b, cls))

class ProjectPermissions(Flag):
    "Permissions group for Projects."

    EDIT            = 0b000001
    DELETE          = 0b000010
    VIEW            = 0b000100
    ADD_PROFILE     = 0b001000
    EDIT_PROFILE    = 0b010000
    REMOVE_PROFILE  = 0b100000
    

    @classmethod
    def default(cls):
        return cls.VIEW
    
    @classmethod
    def all(cls):
        return _flag_all(cls)

class ProfilePermissions(Flag):
    "Permissions group for Profiles."

    READ            = 0b001
    WRITE           = 0b010
    EDIT            = 0b100

    @classmethod
    def default(cls):
        return cls.READ
    
    @classmethod
    def all(cls):
        return _flag_all(cls)