import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ip_verification_module import verify_mac_address, verify_ipv4_address
from simulation.ethernet_frame import EthernetFrame

class Switch:
	def __init__(self, name: str, ipv4_address: str, mac_address: str):
		if not isinstance(name, str):
			raise ValueError("L'identificativo dello switch deve essere una stringa.")
			
		ipv4_validation = verify_ipv4_address(ipv4_address)
		if ipv4_validation["success"] == False:
			raise ValueError(ipv4_validation["error"])
		
		mac_address_validation = verify_mac_address(mac_address)
		if mac_address_validation["success"] == False:
			raise ValueError(mac_address_validation["error"])
			
		self.name = name
		self.ipv4_address = ipv4_address
		self.mac_address = mac_address
		self.mac_table = {}
	
	def receive_frame(self, frame: EthernetFrame):
		if not isinstance(frame, EthernetFrame):
			raise ValueError("IL pacchetto non può essere inoltrato correttamente")
		
		self.mac_table[frame.source_mac_address] = frame.source_host
		
		if frame.destination_mac_address in self.mac_table.keys():
			self.mac_table[frame.destination_mac_address].receive(frame)
		else:
			for mac, host in self.mac_table:
				if host != frame.source_host:
					host.receive(frame)
		
			
