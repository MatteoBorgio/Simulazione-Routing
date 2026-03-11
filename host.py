class Host:
	def __init__(self, host_name: str, mac_address: str, ipv4_address: str, ipv6_address: str):
		self.valid_hex_char = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
		if not isinstance(host_name, str):
			raise ValueError("L'identificativo dell'host deve essere una stringa.")
		
		mac_address_validation = self.verify_mac_address(mac_address)
		if mac_address_validation["success"] == False:
			raise ValueError(mac_address_validation["error"])
		
		ipv4_validation = self.verify_ipv4_address(ipv4_address)
		if ipv4_validation["success"] == False:
			raise ValueError(ipv4_validation["error"])
		
		ipv6_validation = self.verify_ipv6_address(ipv6_address)
		if ipv4_validation["success"] == False:
			raise ValueError(ipv4_validation["error"])
					
		self.host_name = host_name
		self.mac_address = mac_address
		self.ipv4_address = ipv4_address
		self.ipv6_address = ipv6_address
		
		self.subnet_mask = self.calculate_subnet_mask(self.ipv4_address)
		self.arp_table = {}
		
	def verify_mac_address(self, mac_address: str) -> dict[str, bool | str]:
		if not isinstance(mac_address, str):
			return {"success": False, "error": "Il mac address deve essere una stringa."}
		valid_mac_address_model = "XX:XX:XX:XX:XX:XX"
		if len(mac_address) != len(valid_mac_address_model):
			return {"success": False, "error": "Il mac address deve seguire il modello XX:XX:XX:XX:XX:XX"}
		for i in range(len(mac_address)):
			if valid_mac_address_model[i] == ":" and mac_address[i] != ":":
				return {"success": False, "error": "Il mac address deve seguire il modello XX:XX:XX:XX:XX:XX"}
			if mac_address[i].upper() not in self.valid_hex_char and valid_mac_address_model[i] != ":":
				return {"success": False, "error": "Il mac address può contenere solo caratteri esagesimali"}
		return {"success": True}
	
	def verify_ipv4_address(self, ipv4_address: str) -> dict[str, bool | str]:
		if not isinstance(ipv4_address, str):
			return {"success": False, "error": "L'indirizzo ipv4 deve essere una stringa"}
		valid_ipv4_char = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
		ipv4_octets = ipv4_address.split(".")
		if len(ipv4_octets) != 4:
			return {"success": False, "error": "L'indirizzo ipv4 deve essere rappresentato da 4 ottetti"}
		for octet in ipv4_octets:
			for char in octet:
				if char not in valid_ipv4_char:
					return {"success": False, "error": "L'indirizzo ipv4 deve contenere solo caratteri numerici"}
				if int(octet) >= 256:
					return {"success": False, "error": "Ogni ottetto di un indirizzo ipv4 non può superare il numero 255"}
		return {"success": True}
		
	def verify_ipv6_address(self, ipv6_address: str) -> dict[str, str | bool]:
		if not isinstance(ipv6_address, str):
			return {"success": False, "error": "L'indirizzo ipv6 deve essere una stringa"}
		if ipv6_address.count("::") > 1:
			return {"success": False, "error": "L'indirizzo IPv6 può contenere al massimo un gruppo vuoto (::)"}
		ipv6_groups = ipv6_address.split(":")
		if "" in ipv6_groups:
			index = ipv6_groups.index("")
			groups_missing = 8 - (len(ipv6_groups) - 1)
			ipv6_groups = ipv6_groups[:index] + ["0000"]*groups_missing + ipv6_groups[index+1:]
		if len(ipv6_groups) != 8:
			return {"success": False, "error": "L'indirizzo ipv6 deve essere rappresentato da otto gruppi di caratteri esadecimali"}
		for group in ipv6_groups:
			for char in group:
				if char.upper() not in self.valid_hex_char:
					return {"success": False, "error": "L'indirizzo ipv6 deve contenere solo caratteri esadecimali"}
		return {"success": True}
		
	def calculate_subnet_mask(self, ipv4_address: str) -> str:
		ipv4_octets = ipv4_address.split(".")
		if int(ipv4_octets[0]) <= 127:
			return "255.0.0.0"
		elif int(ipv4_address[0]) > 127 and int(ipv4_address[0]) <=191:
			return "255.255.0.0"
		else:
			return "255.255.255.0"
	
if __name__ == "__main__":
	host = Host(
	host_name="Host1",
	mac_address="01:23:45:AB:CD:EF",
	ipv4_address="192.168.0.1",
	ipv6_address="2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    )
	print(host.host_name)
	print(host.mac_address)
	print(host.ipv4_address)
	print(host.ipv6_address)
	print(host.arp_table)
	print(host.subnet_mask)
	print("Host creato con successo!")
