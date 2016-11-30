'''
nameserver.py

Author: Daichi Mae
Author: Shravya shama Bhandari
'''

from message import Message
from redord import ResourceRecord

class NameServer(object):
    """
    A simple DNS server.
    """

    def start():
        """
        Start the server.
        """
        while(True):
            # create a socket object on UDP 53
            packet = "THIS IS A UDP PACKET"

            message = readMessage(packet)

            # if the message if a query
            if message.flags[0] == 0:
                reply = message
                reply.flags[0] = 1
                for question in message.questions:
                    answer = lookup(question)
                    if answer is not None:
                        reply.answers.append(answer)
                    else:
                        # if lookup(suffix of the name in the question) is None
                        # then send a query to a root DNS server and wait for
                        # a reply and put the reply in the cache

                        # if lookup(suffix of the name in the question) is None
                        # then send a query to a TLD server and wait for a
                        # reply and put the reply in the cache

                        # send a query to an authoritive server, wait for a
                        # reply and then put the reply in the cache

                        # reply.answers.append(answer)
                    # send a reply to the client
            

    def readMessage(packet):
        """
        Create a Message object from a UDP packet.

        @param packet: UDP packet
        @return: Message object
        """
        pass

    def createPacket(message):
        """
        Create a DNS message as a UDP packet from a Message object.

        @param message: Mesasge object
        @return: UDP packet
        """
        pass

    def lookup(question):
        """
        Lookup a resource record for a question in the cache. If there's a
        record for the question, return the ResourceRecord object. Otherwise
        return None.
        
        @param queston: question as a partially filled ResourceRecord object
        @return: answer for the question as a ResourceRecord object or None
        """
        pass
    
    
def main():
    NameServer().start()

if __name__ == "__main__":
    main()
