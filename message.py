'''
message.py

Author: Daichi Mae
Author: Shravya shama Bhandari
'''

class Message(object):
    """
    This class represents a DNS message.

    rid (int): Identification number
    flags (list): [0] (int): QR - Query(0)/Reply(1)
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

    __slots__ = ( "rid", "flags", "questions", "answers", "authorities",
                  "additionalRecords")

    # TYPE values
    A = 1
    NS = 2
    CNAME = 5
    MX = 15

    # CLASS values
    IN = 1

    def __init__(self):
        #print("constructing a message")
        self.rid = 0
        self.flags = [0] * 8
        self.questions = []
        self.answers = []
        self.authorities = []
        self.additionalRecords = []
                    
    def __str__(self):
        s = ("Message:\n" +
        "  ID={0}\n".format(self.rid) +
        "  QR={0}\n".format(self.flags[0]) +
        "  OPCODE={0}\n".format(self.flags[1]) +
        "  AA={0}\n".format(self.flags[2]) +
        "  TC={0}\n".format(self.flags[3]) +
        "  RD={0}\n".format(self.flags[4]) +
        "  RA={0}\n".format(self.flags[5]) +
        "  QR={0}\n".format(self.flags[6]) +
        "  RCODE={0}\n".format(self.flags[7]))
        s += "  QUESTIONS:\n"
        for question in self.questions:
           s = s + "    " + str(question) + "\n"
        s += "  ANSWERS:\n"
        for asnwer in self.answers:
           s = s + "    " + str(answer) + "\n"
        s += "  AUTHORITIES:\n"
        for auth in self.authorities:
           s = s + "    " + str(auth) + "\n"
        s += "  ADDITIONAL RECORDS:\n"
        for ar in self.additionalRecords:
           s = s + "    " + str(ar) + "\n"
        return s
