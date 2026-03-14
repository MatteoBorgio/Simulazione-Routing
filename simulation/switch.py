import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ip_verification_module import verify_mac_address, verify_ipv4_address

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
		self.mac_table = []
	
	def verify_if_in_mac_table(self, mac_address_to_verify: str):
		if mac_address_to_verify in self.mac_table:
			return True
		else return False
	
	def add_to_mac_table(self, mac_address_to_add):
		if mac_address_to_add not in self.mac_table:
			self.mac_table.append(mac_address_to_add)
	
	
