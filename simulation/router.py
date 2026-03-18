import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ip_verification_module import verify_mac_address, verify_ipv4_address

class Router:
	def __init__(self, name: str, public_ipv4_address: str, private_ipv4_address: str, mac_address: str):
		if not isinstance(name, str):
			raise ValueError("L'identificativo del router deve essere una stringa.")
			
		mac_address_validation = verify_mac_address(mac_address)
		if mac_address_validation["success"] == False:
			raise ValueError(mac_address_validation["error"])
		
		private_ipv4_validation = verify_ipv4_address(private_ipv4_address)
		if private_ipv4_validation["success"] == False:
			raise ValueError(private_ipv4_validation["error"])
			
		
		public_ipv4_validation = verify_ipv4_address(public_ipv4_address)
		if public_ipv4_validation["success"] == False:
			raise ValueError(public_ipv4_validation["error"])
			
		self.name = name
		self.public_ipv4_address = public_ipv4_address
		self.private_ipv4_address = private_ipv4_address
		self.mac_address = mac_address
		
	def __str__(self):
		return f"Router: {self.name}\nMac: {self.mac_address}\nIpv4: {self.public_ipv4_address}\nPrivate ipv4: {self.private_ipv4_address}"
		
		
