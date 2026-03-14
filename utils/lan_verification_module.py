from utils.ip_verification_module import verify_ipv4_address

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
