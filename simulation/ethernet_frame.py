import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.packet import Packet
from utils.ip_verification_module import verify_mac_address

class EthernetFrame:
	def __init__(self, source_host: "Host", destination_mac_address: str, content_payload: Packet):
		# Import locale per evitare import circolari
		from simulation.host import Host
		
		destination_mac_address_validation = verify_mac_address(destination_mac_address)
		if destination_mac_address_validation["success"] == False:
			raise ValueError(destination_mac_address_validation["error"])
			
		if not isinstance(content_payload, Packet):
			raise ValueError("Il contenuto del frame deve essere un pacchetto")
			
		if not isinstance(source_host, Host):
			raise ValueError("L'host deve essere un'istanza di Host")
		
		self.destination_mac_address = destination_mac_address
		self.content_payload = content_payload
		self.source_host = source_host
		
	def __str__(self):
		return f"Source Host: {self.source_host.name}\nSource Mac: {self.source_host.mac_address}\nDestination Mac: {self.destination_mac_address}\nPayload: {self.content_payload}"
