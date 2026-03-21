import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ip_verification_module import verify_ipv4_address
from simulation.packet import TCPPacket
from enum import Enum
from random import randint

class State(Enum):
	CLOSED = "CLOSED"
	LISTEN = "LISTEN"
	SYN_SENT = "SYN_SENT"
	SYN_RECEIVED = "SYN RECEIVED"
	ESTABLISHED = "ESTABLISHED"
	FIN_WAIT = "FIN_WAIT"	
	CLOSE_WAIT = "CLOSE WAIT"
	
class TCPSession:
	def __init__(self, host: "Host", target_ip: str, target_port: int, source_port: int):
		
		target_ip_validation = verify_ipv4_address(target_ip)
		if target_ip_validation["success"] == False:
			raise ValueError(target_ip_validation["error"])
		
		if not isinstance(target_port, int) or not isinstance(source_port, int):
			raise ValueError("La porta deve essere un intero")
		
		self.target_ip = target_ip
		self.target_port = target_port
		self.source_port = source_port
		self.state = State.CLOSED
		self.host = host
		self.my_sequence_number = randint(1, 1000)
		self.expected_ack_num = 0
		self.transmission_buffer = {}
		self.reception_buffer = {}
		
	def connect(self):
		self.state = State.SYN_SENT
		packet = TCPPacket(source_ip=self.host.ipv4_address, destination_ip=self.target_ip, content_payload="", source_port=self.source_port, destination_port=self.target_port, sequence_number=self.my_sequence_number, acknowledgement_number=self.expected_ack_num, syn=True, acknowledgement=False)
		self.transmission_buffer[self.my_sequence_number] = packet
		self.my_sequence_number += 1
		self.host.send_packet(self.target_ip, packet, "tcp")
	
	def handle_received_packet(self, packet: TCPPacket):
		if self.state == State.LISTEN and packet.syn and packet.acknowledgement == False:
			self.expected_ack_num = packet.sequence_number + 1
			self.state = State.SYN_RECEIVED
			response_packet = TCPPacket(source_ip=self.host.ipv4_address, destination_ip=self.target_ip, content_payload="TCP Packet", source_port=self.source_port, destination_port=self.target_port, sequence_number=self.my_sequence_number, acknowledgement_number=self.expected_ack_num, syn=True, acknowledgement=True)
			self.transmission_buffer[self.my_sequence_number] = response_packet
			self.my_sequence_number += 1
			self.host.send_packet(self.target_ip, response_packet, "tcp")
		elif self.state == State.SYN_SENT and packet.syn == True and packet.acknowledgement:
			self.expected_ack_num = packet.sequence_number + 1
			self.state = State.ESTABLISHED
			response_packet = TCPPacket(source_ip=self.host.ipv4_address, destination_ip=self.target_ip, content_payload="TCP Packet", source_port=self.source_port, destination_port=self.target_port, sequence_number=self.my_sequence_number, acknowledgement_number=self.expected_ack_num, syn=False, acknowledgement=True)
			self.transmission_buffer[self.my_sequence_number] = response_packet
			self.my_sequence_number += 1
			self.host.send_packet(self.target_ip, response_packet, "tcp")
		elif self.state == State.SYN_RECEIVED and packet.syn == False and packet.acknowledgement:
			self.state = State.ESTABLISHED
