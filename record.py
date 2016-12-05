'''
record.py

Author: Daichi Mae
Author: Shravya shama Bhandari
'''

class ResourceRecord(object):
    """
    This class represents a resource record.

    name (str): the name that is being queried/answered
    rtype (int): TYPE value
    rclass (int): CLASS value
    ttl (int): the time interval that the resource record may be cached before
               the source of the information should again be consulted
    rdlength (int): the length of the RDATA field
    rdata (str): a variable length string that describes the resource
    """
    
    __slots__ = ( "name", "rtype", "rclass", "ttl", "rdlength", "rdata")

    # TYPE values
    A = 1
    NS = 2
    CNAME = 5
    MX = 15

    # CLASS values
    IN = 1

    def __init__(self, name=None, rtype=None, rclass=None, ttl=None,
                 rdlength=None, rdata=None):
        self.name = name
        self.rtype = rtype
        self.rclass = rclass
        self.ttl = ttl
        self.rdlength = rdlength
        self.rdata = rdata

    def __str__(self):
        return "NAME={0}, TYPE={1}, CLASS={2}, TTL={3}, RDLENGTH={4}, RDATA={5}".format(self.name, self.rtype, self.rclass, self.ttl, self.rdlength, self.rdata)
