'''
nameserver.py

Author: Daichi Mae
Author: Shravya shama Bhandari
'''

import socket
import sys
import random
from message import Message
from record import ResourceRecord
from dnslib.dns import *

class NameServer(object):
    """
    A simple recursive DNS server.

    cache (list): stores mappings as ResourceRecord objects 
    """
    __slots__ = "cache", "sock"
    
    rootServers = ("198.41.0.4", "192.228.79.201", "192.33.4.12",
                   "199.7.91.13", "192.203.230.10", "192.5.5.241",
                   "192.112.36.4", "198.97.190.53", "192.36.148.17",
                   "192.58.128.30", "193.0.14.129", "199.7.83.42",
                   "202.12.27.33") # a through m

    def __init__(self):
        self.cache = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        

    def start(self):
        """
        Start the server.
        """
        while(True):
            message, client = self.receiveMessage()
           
            # if the message if a query
            if message.flags[0] == 0:
                reply = Message()
                reply.rid = message.rid
                reply.flags[0] = 1
                for question in message.questions:
                    # check if the answer is in the cache
                    answer = self.lookup(question)
                    if answer is not None:
                        reply.answers.append(answer)
                    else: # the answer is not in the cache
                        # get the IP addresses for a TLD server responsible
                        # for the suffix
                        rootQuestion = ResourceRecord(
                            question.name.split(".")[-1], question.rtype,
                            question.rclass)
                        rootRecord = self.lookup(rootQuestion)
                        if rootRecord is None:
                            print("Sending a query to a root DNS server...")
                            rootQuery = Message()
                            rootQuery.rid = message.rid
                            rootQuestion.name = question.name
                            rootQuery.questions.append(rootQuestion)
                            self.sendMessage(rootQuery,
                                         random.choice(NameServer.rootServers))
                            rootReply = Message()
                            # wait for a reply to the query
                            while(not(rootReply.rid==message.rid
                                      and rootReply.flags[0]==1)):
                                rootReply, sender = self.receiveMessage()
                            rootRecord = ResourceRecord(
                                rootReply.authorities[0].name,
                                rootReply.additionalRecord[0].rtype,
                                rootReply.additionalRecord[0].rclass,
                                rootReply.additionalRecord[0].ttl,
                                rootReply.additionalRecord[0].rdlength,
                                rootReply.additionalRecord[0].rdata)
                            self.cache.append(rootRecord)

                        # get the IP addresses for an authority server
                        # responsible for the domain
                        tldQuestion = ResourceRecord(
                            question.name.split(".")[-2] + "."
                            + question.name.split(".")[-1],
                        question.rtype, queston.rclass)
                        tldRecord = self.lookup(tldQuestion)
                        if tldRecord is None:
                            print("Sending a query to a TLD DNS server...")
                            tldQuery = Message()
                            tldQuery.rid = message.rid
                            tldQuestion.name = question.name
                            tldQuery.questions.append(tldQuestion)
                            self.sendMessage(tldQuery, rootRecord.rdata)
                            # wait for a reply to the query
                            while(not(tldReply.rid==message.rid
                                      and tldReply.flags[0]==1)):
                                tldReply, sender = self.receiveMessage()
                            tldRecord = ResourceRecord(
                                tldReply.authorities[0].name,
                                tldReply.additionalRecord[0].rtype,
                                tldReply.additionalRecord[0].rclass,
                                tldReply.additionalRecord[0].ttl,
                                tldReply.additionalRecord[0].rdlength,
                                tldReply.additionalRecord[0].rdata)
                            self.cache.append(tldRecord)
                            
                        # get the IP addresses for a hostname to the authority
                        # server
                        print("Sending a query to an authoritative DNS server...")
                        authQuery = Message()
                        authQuery.rid = message.rid
                        authQuery.questions.append(question)
                        self.sendMessage(authQuery, tldRecord.rdata)
                        # wait for a reply to the query
                        while(not(authReply.rid==message.rid
                                  and authReply.flags[0]==1)):
                            authReply, sender = self.receiveMessage()
                        for answer in authReply.answers:
                            self.cache.append(answer)
                            reply.answers.append(answer)
                sendMessage(reply, client)

    def receiveMessage(self):
        """
        Receive a DNS message and return a tuple of a Message object and the 
        IP address of the sender.

        @return: (Message object, IP address of the sender (str))
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        
        s.bind(("129.21.122.121", 53)) # interface's IP address
        data, addr = s.recvfrom(512)
        d = DNSRecord.parse(data)

        message = Message()
        message.rid = d.header.id
        for question in d.questions:
            message.questions.append(ResourceRecord(str(question.qname)[:-1],
                                                    question.qtype,
                                                    question.qclass))
        for answer in d.rr:
            message.answers.append(ResourceRecord(str(answer.rname)[:-1],
                                                  answer.rtype,
                                                  answer.rclass,
                                                  answer.ttl,
                                                  answer.rdlength,
                                                  answer.rdata))
        for a in d.auth:
            message.authorities.append(ResourceRecord(str(a.rname)[:-1],
                                                      a.rtype,
                                                      a.rclass,
                                                      a.ttl,
                                                      a.rdlength,
                                                      a.rdata))
        for a in d.ar:
            message.additionalRecords.append(ResourceRecord(str(a.rname)[:-1],
                                                            a.rtype,
                                                            a.rclass,
                                                            a.ttl,
                                                            a.rdlength,
                                                            a.rdata))
        print("Received a message from {0}.".format(addr[0]))
        print(message)
        return message, addr

    def sendMessage(self, message, destination):
        """
        Send a DNS message.

        @param message (Message): Mesasge object
        @param destination (str): IP address of the destination
        """
        print("Sending a message to {0}".format(destination))
        print(message)

        d = DNSRecord()
        for question in message.questions:
            d.add_question(DNSQuestion(question.name))
        for answer in message.answers:
            d.add_answer(RR(answer.name, answer.rtype, ttl=answer.ttl, rdata=A(answer.rdata)))
        for auth in message.authorities:
            d.add_auth(RR(auth.name, auth.rtype, ttl=auth.ttl, rdata=A(auth.rdata)))
        for ar in message.additionalRecords:
            d.add_ar(RR(ar.name,ttl=ar.ttl,rdata=A(ar.rdata)))
        
        self.sock.sendto(d.pack(), (destination, 53))

    def lookup(self, question):
        """
        If there's an answer in the cache for the question return the 
        ResourceRecord object. Otherwise return None.
        
        @param queston: question as a partially filled ResourceRecord object
        @return: ResourceRecord object or None
        """
        for record in self.cache:
            if record.name == question.name and record.rtype == question.rtype and record.rclass == question.rclass:
                return record
        return None
    
def main():
    NameServer().start()

if __name__ == "__main__":
    main()
