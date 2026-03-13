valid_hex_char = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

def verify_mac_address(mac_address: str) -> dict[str, bool | str]:
		if not isinstance(mac_address, str):
			return {"success": False, "error": "Il mac address deve essere una stringa."}
		valid_mac_address_model = "XX:XX:XX:XX:XX:XX"
		if len(mac_address) != len(valid_mac_address_model):
			return {"success": False, "error": "Il mac address deve seguire il modello XX:XX:XX:XX:XX:XX"}
		for i in range(len(mac_address)):
			if valid_mac_address_model[i] == ":" and mac_address[i] != ":":
				return {"success": False, "error": "Il mac address deve seguire il modello XX:XX:XX:XX:XX:XX"}
			if mac_address[i].upper() not in valid_hex_char and valid_mac_address_model[i] != ":":
				return {"success": False, "error": "Il mac address può contenere solo caratteri esagesimali"}
		return {"success": True}

def verify_ipv4_address(ipv4_address: str) -> dict[str, bool | str]:
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
		
def verify_ipv6_address(ipv6_address: str) -> dict[str, str | bool]:
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
				if char.upper() not in valid_hex_char:
					return {"success": False, "error": "L'indirizzo ipv6 deve contenere solo caratteri esadecimali"}
		return {"success": True}
		
def verify_if_is_in_the_same_lan(ipv4_controller_address: str, controller_subnet_mask: str, ipv4_address_to_verify: str):
	ipv4_validation = verify_ipv4_address(ipv4_controller_address)
	if ipv4_validation["success"] == False:
		raise ValueError(ipv4_validation["error"])
		
	ipv4_validation = verify_ipv4_address(ipv4_address_to_verify)
	if ipv4_validation["success"] == False:
		raise ValueError(ipv4_validation["error"])
		
	subnet_mask_validation = verify_ipv4_address(controller_subnet_mask)
	if subnet_mask_validation["success"] == False:
		raise ValueError(subnet_mask_validation["error"])
		
	ipv4_controller_octets = ipv4_controller_address.split(".")
	ipv4_to_verify_octets = ipv4_address_to_verify.split(".")
	subnet_mask_octets = controller_subnet_mask.split(".")
	
	ipv4_controller_mask_applied = []
	ipv4_address_to_verify_mask_applied = []
	
	for i in range(4):
		ipv4_controller_mask_applied.append(str(int(ipv4_controller_octets[i]) & int(subnet_mask_octets[i])))
		ipv4_address_to_verify_mask_applied.append(str(int(ipv4_to_verify_octets[i]) & int(subnet_mask_octets[i])))

	ipv4_controller_comparison_string = ".".join(ipv4_controller_mask_applied)
	ipv4_address_to_verify_comparison_string = ".".join(ipv4_address_to_verify_mask_applied)
	
	return ipv4_address_to_verify_comparison_string == ipv4_controller_comparison_string
	
			
	
	
	
