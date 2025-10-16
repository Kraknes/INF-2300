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
        self.window = []
        self.pack_num = 0
        self.pack_buffer_list = []

    def with_logger(self, logger):
        self.logger = logger
        return self

    def register_above(self, layer):
        self.application_layer = layer

    def register_below(self, layer):
        self.network_layer = layer
    
    # Made by student
    ## Prepares checksum for packet
    def checksum_calculation(self, binary_data):
        hasher = hashlib.sha256(binary_data)
        hasher = hasher.hexdigest()
        return hasher

    # Made by student
    ## Prepares packet with right attribute
    def prepare_packet(self, packet):
        packet.checksum = self.checksum_calculation(packet.data)
        packet.number = self.pack_num
        self.pack_num += 1

    # Made by student
    ## Timer function to resend packets
    def resend_packets(self):
        print(f"{self.logger.name} is resending packets")
        if len(self.window) == 0:
            self.timer.cancel()
            self.timer = None
            return
        for x in self.window:
            self.network_layer.send(x)
        self.reset_timer(self.resend_packets)
    
    # Made by student 
    ## Creates and sends ACK or NACK back 
    def send_acknack(self, packet, bool):
        ack = copy(packet)
        ack.ACK = bool
        self.network_layer.send(ack)

    # # Made by student
    # ## Sorting function based on item number
    # def sortFunc(self, item):
    #     return item.number
    
    # Made by student
    ## Sends boolean based on checksum
    def checksum_status(self, packet):
        if packet.checksum == self.checksum_calculation(packet.data):
            return True
        if packet.checksum != self.checksum_calculation(packet.data):
            return False

    def from_app(self, binary_data):
        packet = Packet(binary_data)

        # Implement me!
        self.prepare_packet(packet) # Adds checksum and numbers

        if len(self.window) <= 5: # Window is size of 5
            self.window.append(packet)
            print(f"{self.logger.name} has sent {packet}")
            self.network_layer.send(packet)
        else:
            self.pack_buffer_list.append(packet)

        self.reset_timer(self.resend_packets)

    def from_network(self, packet):

        # Data packet received
        if packet.ACK == None:

            ## If an already processed package
            if packet.number < self.pack_num: 
                self.send_acknack(packet, True)
                return
            
            ## If corrupted data
            if self.checksum_status(packet) == False:
                print(f"{self.logger.name} sendt NACK for {packet}")
                self.send_acknack(packet, False)

            ## If normal data
            elif self.checksum_status(packet) == True: 
                if packet.number == self.pack_num:
                    print(f"{self.logger.name} has received {packet}")
                    self.application_layer.receive_from_transport(packet.data)
                    self.pack_num += 1
                    print(f"{self.logger.name} sendt ACK for {packet}")
                    self.send_acknack(packet, True)
    
        # ACK packet received
        elif packet.ACK == True:
            for x in self.window:
                if x.number == packet.number:
                    self.window.remove(x)
                    print(f"{self.logger.name} received ACK for {packet}")

        # NACK packet received
        elif packet.ACK == False:
            for x in self.window:
                if x.number == packet.number:
                    self.network_layer.send(x)
                    print(f"{self.logger.name} received NACK for {packet}")

        # Adds from packet buffer list to window 
        while len(self.window) <= 5 and len(self.pack_buffer_list) > 0:
            self.window.append(self.pack_buffer_list[0])
            self.pack_buffer_list.pop(0)


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
