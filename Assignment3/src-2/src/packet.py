class Packet:
    """Represent a packet of data.
    Note - DO NOT REMOVE or CHANGE the data attribute!
    The simulation assumes this is present!"""

    def __init__(self, binary_data):
        # Add which ever attributes you think you might need
        # to have a functional packet.
        # TIPS: Add a __str__ method to print a packet-object nicely! :)
        # Extend me!
        self.data = binary_data
        self.checksum = None
        self.number = None
        self.ACK = None
        
    def __str__(self):
        return "Packet data: " + str(self.data) + ", Packet number: " + str(self.number)
