from copy import copy
from threading import Timer

from packet import Packet
import hashlib



class TransportLayer:
    """The transport layer receives chunks of data from the application layer
    and must make sure it arrives on the other side unchanged and in order.
    """

    def __init__(self):
        self.timer = None
        self.timeout = 0.4  # Seconds
        self.packetBuffer = []
        self.packetOut = []
        self.packetTot = []
        self.packConfirmed = 0
        self.next_pck_nr = 0

    def with_logger(self, logger):
        self.logger = logger
        return self

    def register_above(self, layer):
        self.application_layer = layer

    def register_below(self, layer):
        self.network_layer = layer

    ## Created by student, checksum calculcation for packets
    def checksum_calculation(self, binary_data):
        hasher = hashlib.sha256(binary_data)
        hasher = hasher.hexdigest()
        return hasher
    
    ## Created by student, sorting of list
    def sortFunc(self, item):
        return item.number
    
    ## Created by student, timer to send all packets in list
    def resend_packets(self, packetList):
        print(f"{self.logger.name} Time limit! Resending packet.")
        if len(self.packetOut) == 0 and self.timer:
            self.timer.cancel()
            self.timer = None
            return
        for x in packetList:
            # print(f"Resending {x}!")
            self.network_layer.send(x)
        self.reset_timer(self.resend_packets, (packetList,))

    def from_app(self, binary_data):
        # Implement me!
        number = self.next_pck_nr
        self.next_pck_nr += 1
        checksum = self.checksum_calculation(binary_data)
        packet = Packet(binary_data, number, checksum)
        self.packetTot.append(packet)

        # Adds packet to send out or to buffer list
        if len(self.packetOut) <= 5: # If list is less < 5 (only the five first of all packets)
            self.packetOut.append(packet)
            print(f"{self.logger.name} sends {packet}!")
            self.network_layer.send(packet) # Sends packet
        else:
            print(f"{self.logger.name} adds {packet} to buffer list!")
            self.packetBuffer.append(packet)
            
        if self.timer == None:
            self.reset_timer(self.resend_packets, (self.packetOut,))

    def send_data_to_app(self):
        for x in self.packetTot:
            if self.packConfirmed == x.number:
                self.packConfirmed += 1  
                self.application_layer.receive_from_transport(x.data)

    def data_packet(self, packet):
        checksum = self.checksum_calculation(packet.data)
           
        # If data packet is OK, send to application and ACK back
        if checksum == packet.checksum:
            # If new packet, sends to application and ACK
            if self.packConfirmed == packet.number:
                # self.packetTot.append(packet) 
                self.packConfirmed += 1  
                print(f"{self.logger.name} has sendt {packet} to Application")
                self.application_layer.receive_from_transport(packet.data)
                ack = copy(packet)
                ack.ACK = True
                print(f"{self.logger.name} sends ACK for {packet}!")
                self.network_layer.send(ack)
            # If old packet, sends ACK    
            elif self.packConfirmed > packet.number:
                ack = copy(packet)
                ack.ACK = True
                print(f"{self.logger.name} sends ACK for {packet}!")
                self.network_layer.send(ack)
        
        # Corrupted, sends a NACK back.     
        else:
            nack = copy(packet)
            nack.ACK = False
            print(f"{self.logger.name} sends NACK for {packet}!")
            self.network_layer.send(nack)

        ## For loop for sending packets to application. Must be in correct order!
        # self.packetTot.sort(key=self.sortFunc)
        # for x in self.packetTot:
        #     if x.number == self.packConfirmed:
        #         print(f"{self.logger.name} has sendt {x} to Application")
        
        #         self.packConfirmed += 1
        #         self.application_layer.receive_from_transport(x.data)


    # Alice function, ACK or NACK
    def ack_or_nack(self, packet):
        ## If ACK from Bob
        if packet.ACK == True:
            for x in self.packetOut:
                if x.number == packet.number: # Removes packet from memory
                    self.packetOut.remove(x)
                    self.packConfirmed += 1
                    print(f"{self.logger.name} receives ACK packet {packet}!")
                    if len(self.packetBuffer) > 0:
                        for x in self.packetBuffer:
                            self.packetOut.append(x)
                            self.packetBuffer.remove(x)
                            print(f"{self.logger.name}Added packet {x} to self.packetOut")
                            print(f"{self.logger.name}Removed packet data {x} from self.packetBuffer")
                    # self.reset_timer(self.send_packets, (self.packetOut,)) # Resets timer
 
        # If NACK from Bob              
        elif packet.ACK == False: 
             for x in self.packetOut:
                if x.number == packet.number: # Removes packet from memory
                    self.network_layer.send(x) # Sends packet


    def from_network(self, packet):
        # Implement me!
        self.send_data_to_app()
       
        ## Checks if packet is data or an ACK/NACK
        if packet.ACK == None:
            self.data_packet(packet)
        else:
            self.ack_or_nack(packet)

    


    def reset_timer(self, callback, *args):
        # This is a safety-wrapper around the Timer-objects, which are
        # separate threads. If we have a timer-object already,
        # stop it before making a new one so we don't flood
        # the system with threads!
        if self.timer:
            if self.timer.is_alive():
                self.timer.cancel()
        # callback(a function) is called with *args as arguments
        # after self.timeout seconds.
        self.timer = Timer(self.timeout, callback, *args)
        self.timer.start()
