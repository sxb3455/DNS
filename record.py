'''
record.py

Author: Daichi Mae
Author: Shravya shama Bhandari
'''

class ResourceRecord(object):
    """
    This class represents a resource record.

    name (str): the name that is being queried/answered
    type (int): TYPE value
    class (int): CLASS value
    ttl (int): the time interval that the resource record may be cached before
               the source of the information should again be consulted
    rdlength (int): the length of the RDATA field
    rdata (str): a variable length string that describes the resource
    """
    
    __slots__ = ( "name", "type", "class", "ttl", "rdlength", "rdata")

    # TYPE values
    A = 1
    NS = 2
    CNAME = 5
    MX = 15

    # CLASS values
    IN = 1
