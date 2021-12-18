from functools import reduce
from typing import List, Tuple


class InvalidType(Exception):
    pass


class Packet(object):
    def __init__(self, version: int, type_id: int, bits: int):
        self.version = version
        self.type_id = type_id
        self.bits = bits
        self.sub_packets = []  # type: List[Packet]

    @classmethod
    def parse_bits(cls, bits: str) -> int:
        return int(bits, 2)

    @classmethod
    def hex_to_bits(cls, hexadecimal: str) -> str:
        # return bin(int(hexadecimal, 16))[2:].zfill(len(hexadecimal) * 4)
        bits = ""
        m = {
            "0": "0000",
            "1": "0001",
            "2": "0010",
            "3": "0011",
            "4": "0100",
            "5": "0101",
            "6": "0110",
            "7": "0111",
            "8": "1000",
            "9": "1001",
            "A": "1010",
            "B": "1011",
            "C": "1100",
            "D": "1101",
            "E": "1110",
            "F": "1111",
        }
        for char in hexadecimal:
            bits += m[char]
        return bits

    def __repr__(self) -> str:
        return f"Packet(version={self.version}, type_id={self.type_id}, subpackets={self.sub_packets})"

    def get_total_bits(self) -> int:
        total = self.bits
        for packet in self.sub_packets:
            total += packet.get_total_bits()
        return total

    def get_sum_of_versions(self) -> int:
        total = self.version
        for packet in self.sub_packets:
            total += packet.get_sum_of_versions()
        return total

    def calculate(self) -> int:
        if self.type_id == 0:
            return sum([p.calculate() for p in self.sub_packets])
        elif self.type_id == 1:
            return reduce(
                lambda a, b: a * b, [p.calculate() for p in self.sub_packets], 1
            )
        elif self.type_id == 2:
            return min([p.calculate() for p in self.sub_packets])
        elif self.type_id == 3:
            return max([p.calculate() for p in self.sub_packets])
        elif self.type_id == 5:
            return (
                1
                if self.sub_packets[0].calculate() > self.sub_packets[1].calculate()
                else 0
            )
        elif self.type_id == 6:
            return (
                1
                if self.sub_packets[0].calculate() < self.sub_packets[1].calculate()
                else 0
            )
        elif self.type_id == 7:
            return (
                1
                if self.sub_packets[0].calculate() == self.sub_packets[1].calculate()
                else 0
            )

        else:
            raise InvalidType


class PacketTypeFour(Packet):
    def __init__(self, version: int, bits: int, number: int):
        super().__init__(version, 4, bits)
        self.number = number

    @classmethod
    def get_literal_value(cls, bits: str) -> Tuple[int, str]:
        curr = bits[:5]
        digit_bits = curr[1:]
        i = 1
        while curr[0] == "1":
            curr = bits[i * 5 : (i + 1) * 5]
            digit_bits += curr[1:]
            i += 1
        rest_of_bits = bits[i * 5 :]
        return (int(digit_bits, 2), rest_of_bits)

    def __repr__(self) -> str:
        return f"Packet(version={self.version}, type_id={self.type_id}, number={self.number}, subpackets={self.sub_packets})"

    def calculate(self) -> int:
        return self.number


def parse_packet(
    packet_str: str,
) -> Packet:
    if not packet_str:
        return packet_str
    version = Packet.parse_bits(packet_str[:3])
    type_id = Packet.parse_bits(packet_str[3:6])
    if type_id == 4:
        literal_value, rest_of_bits = PacketTypeFour.get_literal_value(packet_str[6:])
        size_of_packet = len(packet_str) - len(rest_of_bits)
        return PacketTypeFour(version, bits=size_of_packet, number=literal_value)
    else:
        length_type_id = Packet.parse_bits(packet_str[6])
        if length_type_id == 0:
            length_of_sub_packets_bits = Packet.parse_bits(packet_str[7:22])
            rest_of_bits = packet_str[22:]
            size_of_packet = len(packet_str) - len(rest_of_bits)
            packet = Packet(version, type_id, bits=size_of_packet)
            total_bits = 0
            while total_bits < length_of_sub_packets_bits:
                new_packet = parse_packet(rest_of_bits)
                rest_of_bits = rest_of_bits[new_packet.get_total_bits() :]
                total_bits += new_packet.get_total_bits()
                packet.sub_packets.append(new_packet)
            return packet
        else:
            number_of_sub_packets = Packet.parse_bits(packet_str[7:18])
            rest_of_bits = packet_str[18:]
            size_of_packet = len(packet_str) - len(rest_of_bits)
            packet = Packet(version, type_id, bits=size_of_packet)
            total_subpackets = 0
            while total_subpackets < number_of_sub_packets:
                new_packet = parse_packet(rest_of_bits)
                rest_of_bits = rest_of_bits[new_packet.get_total_bits() :]
                packet.sub_packets.append(new_packet)
                total_subpackets += 1
            return packet


def main():
    with open("data/packets_test.txt") as f:
        for hexadecimal in f:
            packet = parse_packet(Packet.hex_to_bits(hexadecimal.strip()))
            print(
                f"packet version sum for {hexadecimal.strip()} = {packet.get_sum_of_versions()}"
            )
            print(
                f"packet version calculation for {hexadecimal.strip()} = {packet.calculate()}"
            )
            print()


main()
