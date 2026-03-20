import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ip_verification_module import verify_ipv4_address, verify_mac_address

class Packet:
	def __init__(self, source_ip: str, destination_ip: str, content_payload: str):
		source_ip_validation = verify_ipv4_address(source_ip)
		if source_ip_validation["success"] == False:
			raise ValueError(source_ip_validation["error"])
		
		destination_ip_validation = verify_ipv4_address(destination_ip)
		if destination_ip_validation["success"] == False:
			raise ValueError(destination_ip_validation["error"])
		
		if not isinstance(content_payload, str):
			raise ValueError("Il contenuto deve essere un messaggio di testo.")
			
		self.source_ip = source_ip
		self.destination_ip = destination_ip
		self.protocol = None
		self.content_payload = content_payload
		self.received = False
		
	def __str__(self):
		return f"Source ipv4: {self.source_ip}\nDestination ipv4: {self.destination_ip}\nProtocol: {self.protocol}\nContent: {self.content_payload}"

class TCPPacket(Packet):
	def __init__(self, source_ip: str, destination_ip: str, content_payload: str, sequence_number=0, acknowledgment_number=0, syn=False, acknowledgement=False):
		super().__init__(source_ip, destination_ip, content_payload)
		
		self.sequence_number = sequence_number
		self.acknowledgement_number = acknowledgement_number
		self.acknowledgement = acknowledgement
		self.syn = syn
		self.protocol = "TCP"
		
	def __str__(self):
		return f"Source ipv4: {self.source_ip}\nDestination ipv4: {self.destination_ip}\nProtocol: {self.protocol}\nContent: {self.content_payload}\nSequence number: {self.sequence_number}"
		
class UDPPacket(Packet):
	def __init__(self, source_ip: str, destination_ip: str, content_payload: str):
		super().__init__(source_ip, destination_ip, content_payload)
		
		self.protocol = "UDP"

class ArpRequest(Packet):
	def __init__(self, source_ip: str, source_mac: str, destination_ip: str, content_payload: str):
		super().__init__(source_ip, destination_ip, content_payload)
		
		mac_address_validation = verify_mac_address(source_mac)
		if mac_address_validation["success"] == False:
			raise ValueError(mac_address_validation["error"])
		
		self.source_mac = source_mac
		self.protocol = "ARP"
		
	def __str__(self):
		return f"Source Mac: {self.source_mac}\nSource ipv4: {self.source_ip}\nDestination ipv4: {self.destination_ip}\nProtocol: {self.protocol}\nContent: {self.content_payload}"






















