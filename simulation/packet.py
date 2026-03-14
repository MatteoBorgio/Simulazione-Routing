import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ip_verification_module import verify_ipv4_address

class Packet:
	def __init__(self, source_ip: str, destination_ip: str, protocol: str, content_payload: str):
		source_ip_validation = verify_ipv4_address(source_ip)
		if source_ip_validation["success"] == False:
			raise ValueError(source_ip_validation["error"])
		
		destination_ip_validation = verify_ipv4_address(destination_ip)
		if destination_ip_validation["success"] == False:
			raise ValueError(destination_ip_validation["error"])
		
		if protocol.lower() not in ["tcp", "udp"]:
			raise ValueError("Protocollo non valido.")
		
		if not isinstance(content_payload, str):
			raise ValueError("Il contenuto deve essere un messaggio di testo.")
			
		self.source_ip = source_ip
		self.destination_ip = destination_ip
		self.protocol = protocol
		self.content_payload = content_payload
		self.received = False
