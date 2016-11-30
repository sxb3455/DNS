'''
message.py

Author: Daichi Mae
Author: Shravya shama Bhandari
'''

class Message(object):
    """
    This class represents a DNS message.

    id (int): Identification number
    flags (list): [0] (int): QR - Query/Reply
                  [1] (int): OPCODE - Operation Code
                  [2] (int): AA - Authoritative Answer
                  [3] (int): TC - TrunCation
                  [4] (int): RD - Recursion Desired
                  [5] (int): RA - Recursion Available
                  [6] (int): Z - Reserved for future use. Must be zero in all 
                                 queries and responses.
                  [7] (int): RCODE - Response Code
    questions (list): Information about the query that is being made. Each
                      question is expressed as a ResourceRecord object.
    answers (list): The resource records for the name that was originally
                    queried. Each question is expressed as a ResourceRecord
                    object.
    authorities (list): Records of other authoritative servers as 
                        ResourceRecord objects.
    additionalRecords (list): Other helpful records as ResourceRecord objects.
    """

    __slots__ = ( "id", "flags", "questions", "answers", "authorities",
                  "additionalRecords")

    # TYPE values
    A = 1
    NS = 2
    CNAME = 5
    MX = 15

    # CLASS values
    IN = 1
