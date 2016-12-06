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

    ifaddr = "129.21.122.81"
    
    rootServers = ("198.41.0.4", "192.228.79.201", "192.33.4.12",
                   "199.7.91.13", "192.203.230.10", "192.5.5.241",
                   "192.112.36.4", "198.97.190.53", "192.36.148.17",
                   "192.58.128.30", "193.0.14.129", "199.7.83.42",
                   "202.12.27.33") # a through m

    def __init__(self):
        self.cache = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((NameServer.ifaddr, 53))

    def start(self):
        """
        Start the server.
        """
        while(True):
            message, client = self.receiveMessage()
            #reply = Message()
            #reply.rid = message.rid
            #reply.questions = message.questions
            #reply.flags[0] = 1
            
            '''
            reply.answers.append(ResourceRecord(message.questions[0].name,
                                                message.questions[0].rtype,
                                                message.questions[0].rclass,
                                                1234,
                                                512,
                                                "5.6.7.8"))
            self.sendMessage(reply, client)
            sys.exit()
            '''
            
           
            # if the message if a query
            if message.flags[0] == 0:
                reply = Message()
                reply.rid = message.rid
                reply.questions = message.questions
                reply.flags[0] = 1
                #reply.flags[2] = 1 # AA FLAG UP
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
                            rootServer = random.choice(NameServer.rootServers)
                            rootQuery = Message()
                            rootQuery.rid = message.rid
                            rootQuestion.name = question.name
                            rootQuery.questions.append(rootQuestion)
                            self.sendMessage(rootQuery, rootServer)
                            rootReply, sender = self.receiveMessage()
                            while(rootServer != sender):
                                rootReply, sender = self.receiveMessage()
                            rootRecord = ResourceRecord(
                                rootReply.authorities[0].name,
                                rootReply.additionalRecords[0].rtype,
                                rootReply.additionalRecords[0].rclass,
                                rootReply.additionalRecords[0].ttl,
                                rootReply.additionalRecords[0].rdlength,
                                rootReply.additionalRecords[0].rdata)
                            self.cache.append(rootRecord)

                        # get the IP addresses for an authority server
                        # responsible for the domain
                        tldQuestion = ResourceRecord(
                            question.name.split(".")[-2] + "."
                            + question.name.split(".")[-1],
                        question.rtype, question.rclass)
                        tldRecord = self.lookup(tldQuestion)
                        if tldRecord is None:
                            print("Sending a query to a TLD DNS server...")
                            tldQuery = Message()
                            tldQuery.rid = message.rid
                            tldQuestion.name = question.name
                            tldQuery.questions.append(tldQuestion)
                            #print("##########################$$$")
                            #print(rootRecord.rdata)
                            self.sendMessage(tldQuery, str(rootRecord.rdata))
                            tldReply, sender = self.receiveMessage()
                            while(str(rootRecord.rdata) != sender):
                                tldReply, sender = self.receiveMessage()
                            # wait for a reply to the query
                            
                            #while(not(tldReply.rid==message.rid
                             #         and tldReply.flags[0]==1)):
                              #  tldReply, sender = self.receiveMessage()
                            tldRecord = ResourceRecord(
                                tldReply.authorities[0].name,
                                tldReply.additionalRecords[0].rtype,
                                tldReply.additionalRecords[0].rclass,
                                tldReply.additionalRecords[0].ttl,
                                tldReply.additionalRecords[0].rdlength,
                                tldReply.additionalRecords[0].rdata)
                            self.cache.append(tldRecord)
                            
                        # get the IP addresses for a hostname to the authority
                        # server
                        print("Sending a query to an authoritative DNS server...")
                        authQuery = Message()
                        authQuery.rid = message.rid
                        authQuery.questions.append(question)
                        self.sendMessage(authQuery, str(tldRecord.rdata))
                        authReply, sender = self.receiveMessage()
                        while(str(tldRecord.rdata) != sender):
                            authReply, sender = self.receiveMessage()
                        # wait for a reply to the query
                        #while(not(authReply.rid==message.rid
                        #          and authReply.flags[0]==1)):
                        #    authReply, sender = self.receiveMessage()
                        for answer in authReply.answers:
                            self.cache.append(answer)
                            reply.answers.append(answer)
                #reply.questions[0].name += "."
                #reply.answers[0].name += "."
                self.sendMessage(reply, client)
                sys.exit()

    def receiveMessage(self):
        """
        Receive a DNS message and return a tuple of a Message object and the 
        IP address of the sender.

        @return: (Message object, IP address of the sender (str))
        """
        #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        
        #s.bind((NameServer.ifaddr, 53))
        #data, addr = s.recvfrom(512)
        data, addr = self.sock.recvfrom(1024)
        
        d = DNSRecord.parse(data)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(d)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        message = Message()
        message.rid = d.header.id
        message.flags[2] = d.header.get_aa()
        for question in d.questions:
            message.questions.append(ResourceRecord(str(question.qname)[:-1],
                                                    question.qtype,
                                                    question.qclass))
        for answer in d.rr:
            message.answers.append(ResourceRecord(str(answer.rname)[:-1],
                                                  answer.rtype,
                                                  answer.rclass,
                                                  answer.ttl,
                                                  None,
                                                  answer.rdata))
        for a in d.auth:
            message.authorities.append(ResourceRecord(str(a.rname)[:-1],
                                                      a.rtype,
                                                      a.rclass,
                                                      a.ttl,
                                                      None,
                                                      a.rdata))
        for a in d.ar:
            message.additionalRecords.append(ResourceRecord(str(a.rname)[:-1],
                                                            a.rtype,
                                                            a.rclass,
                                                            a.ttl,
                                                            None,
                                                            a.rdata))
        print("Received a message from {0}.".format(addr[0]))
        print(message)

        #print("$$$$$$$$$$$$$$$$$$$$$$")
        #print(DNSRecord.parse(d.send("8.8.8.8")))
        #a = d.reply()
        #a.add_answerRR(message.name,QTYPE.A,rdata=A("1.2.3.4"),ttl=60)
        #a.send(addr[0])
        #print("$$$$$$$$$$$$$$$$$$$$$$")
        
        return message, addr[0]

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
            d.add_answer(RR(answer.name, answer.rtype, ttl=answer.ttl, rdata=A(str(answer.rdata))))
        for auth in message.authorities:
            d.add_auth(RR(auth.name, auth.rtype, ttl=auth.ttl, rdata=A(auth.rdata)))
        for ar in message.additionalRecords:
            d.add_ar(RR(ar.name,ttl=ar.ttl,rdata=A(ar.rdata)))

        d.header.id = message.rid
        d.header.set_aa(message.flags[2])
        d.header.set_qr(message.flags[0])
        
        print("QR = {0}".format(d.header.get_qr()))
        print(destination)
        print(d)
        
        self.sock.sendto(d.pack(), (destination, 53))

        '''
        response, sender = self.sock.recvfrom(512)
        print("######## RESPONSE #########")
        print(DNSRecord.parse(response))
        print("##########################")
        '''

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
