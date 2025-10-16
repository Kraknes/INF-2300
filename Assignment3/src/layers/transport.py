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

    def with_logger(self, logger):
        self.logger = logger
        return self

    def register_above(self, layer):
        self.application_layer = layer

    def register_below(self, layer):
        self.network_layer = layer

    ## Created by student, timer to send all packets in list
    def send_packets(self, packetList):
        print(f"Time limit! Resending packets from {self.logger.name}")
        # if self.packConfirmed > 10 and self.timer:
        #     self.timer.cancel()
        #     self.timer = None
        #     return
        for x in packetList:
            # print(f"Resending {x}!")
            self.network_layer.send(x)
        self.reset_timer(self.send_packets, (packetList,))

    ## Created by student, checksum calculcation for packets
    def checksum_calculation(self, binary_data):
        hasher = hashlib.sha256(binary_data)
        hasher = hasher.hexdigest()
        return hasher
    
    ## Created by student, sorting of list
    def sortFunc(self, item):
        return item.number
    

    def from_app(self, binary_data):
        # Implement me!
        number = len(self.packetTot)
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
            self.timer = self.reset_timer(self.send_packets, (self.packetOut,))

    def from_network(self, packet):
        # Implement me!
        # print(f"{self.logger.name} has received {packet}!")
        # If ACK from Bob
        if packet.ACK == True:
            for x in self.packetOut:
                if x.number == packet.number: # Removes packet from memory
                    self.packetOut.remove(x)
                    self.packConfirmed += 1
                    # print(f"{x} removed from {self.logger.name} packetOut list!")
                    if len(self.packetBuffer) > 0:
                        for x in self.packetBuffer:
                            self.packetOut.append(x)
                            self.packetBuffer.remove(x)
                            print(f"Added packet {x} to self.packetOut")
                            print(f"Removed packet data {x} from self.packetBuffer")
                    self.reset_timer(self.send_packets, (self.packetOut,)) # Resets timer
 
        # If NACK from Bob              
        elif packet.ACK == False: 
             for x in self.packetOut:
                if x.number == packet.number: # Removes packet from memory
                    self.network_layer.send(x) # Sends packet
       
        # If Data from Alice
        else: 
            checksum = self.checksum_calculation(packet.data)
            if checksum == packet.checksum:
                data_present = False
                for x in self.packetTot:
                    if x.number == packet.number:
                        data_present = True
                        break
                if not data_present:
                    self.packetTot.append(packet) # puts packet in list
                    
                        
                # Acknowledgement packet send

                ack = copy(packet)
                ack.ACK = True
                # print(f"{self.logger.name} sends ACK for {packet}!")
                self.network_layer.send(ack)

            else:
                # Corrupted, sends a NACK back. 
                nack = copy(packet)
                nack.ACK = False
                # print(f"{self.logger.name} sends NACK for {packet}!")
                self.network_layer.send(nack)

        self.packetTot.sort(key=self.sortFunc)
        for x in self.packetTot:
            if x.number == self.packConfirmed:
                print(f"{self.logger.name} has sendt {x} to Application")
                self.packConfirmed += 1
                self.application_layer.receive_from_transport(x.data)




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
