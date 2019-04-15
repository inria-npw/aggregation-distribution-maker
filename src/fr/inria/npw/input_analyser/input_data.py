import statistics


class InputData:
    def __init__(self):
        self.big_packets = list()

    @property
    def number_of_small_packets(self):
        return sum(self.big_packets)

    @property
    def average_aggregation(self):
        return statistics.mean(self.big_packets)

    def add_big_packet(self, number_of_aggregated_packets):
        self.big_packets.append(number_of_aggregated_packets)
