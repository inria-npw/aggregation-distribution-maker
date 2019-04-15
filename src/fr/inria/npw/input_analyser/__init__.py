import json

from scapy.all import *

from fr.inria.npw.errors import InputFileNotFoundError
from .input_data import InputData


def analyse_json_data(input_file_path):
    """
    :type input_file_path: str
    :rtype: InputData
    :raise FileNotFoundError
    """
    data = InputData()

    try:
        with open(input_file_path, 'r') as input_file:
            json_data = json.load(input_file)
    except FileNotFoundError as e:
        raise InputFileNotFoundError(e)

    number_of_aggregated_packets = 0
    previous_time_received_in_microseconds = 0
    for time_received_in_microseconds in \
            [time_in_nanoseconds / 1000 for time_in_nanoseconds in json_data['timesReceivedInNanoseconds']]:

        delta_time = time_received_in_microseconds - previous_time_received_in_microseconds

        if delta_time > 400:
            if number_of_aggregated_packets != 0:
                data.add_big_packet(number_of_aggregated_packets)

            number_of_aggregated_packets = 0

        number_of_aggregated_packets += 1
        previous_time_received_in_microseconds = time_received_in_microseconds

    if number_of_aggregated_packets != 0:
        data.add_big_packet(number_of_aggregated_packets)

    return data


def analyse_pcap_data(input_file_path):
    """
    :type input_file_path: str
    :rtype: InputData
    :raise FileNotFoundError
    """

    data = InputData()

    try:
        packets = rdpcap(input_file_path)
    except FileNotFoundError as e:
        raise InputFileNotFoundError(e)

    number_of_aggregated_packets = 0
    current_mdpu_value = 0
    for current_packet in packets:
        if current_packet.A_MPDU_flags is None or current_packet.A_MPDU_flags.value != current_mdpu_value:
            if number_of_aggregated_packets != 0:
                data.add_big_packet(number_of_aggregated_packets)

            number_of_aggregated_packets = 0

        number_of_aggregated_packets += 1
        current_mdpu_value = 0 if current_packet.A_MPDU_flags is None else current_packet.A_MPDU_flags.value

    if number_of_aggregated_packets != 0:
        data.add_big_packet(number_of_aggregated_packets)

    return data
