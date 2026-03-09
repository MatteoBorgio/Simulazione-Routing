class Host:
	def __init__(self, host_name: str, mac_address: str, ipv4_address: str, ipv6_address: str):
	 if not isinstance(host_name, str):
		 raise ValueError("L'identificativo dell'host deve essere una stringa.")
		 
	 if not isinstance(mac_address, str):
		 raise ValueError("Il mac address deve essere una stringa.")
	 valid_mac_address_model = "XX:XX:XX:XX:XX:XX"
	 valid_hex_char = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
	 if len(mac_address) != len(valid_mac_address_model):
		 raise ValueError("Il mac address deve seguire il modello XX:XX:XX:XX:XX:XX")
	 for i in range(len(mac_address)):
		 if valid_mac_address_model[i] == ":" and mac_address[i] != ":":
			 raise ValueError("Il mac address deve seguire il modello XX:XX:XX:XX:XX:XX")
		 if mac_address[i].upper() not in valid_hex_char and valid_mac_address_model[i] != ":":
			 raise ValueError("Il mac address può contenere solo caratteri esagesimali")
	 
	 if not isinstance(ipv4_address, str):
		 raise ValueError("L'indirizzo ipv4 deve essere una stringa")
	 valid_ipv4_char = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
	 ipv4_octets = ipv4_address.split(".")
	 if len(ipv4_octets) != 4:
		 raise ValueError("L'indirizzo ipv4 deve essere rappresentato da 4 ottetti")
	 for octet in ipv4_octets:
		 for char in octet:
			 if char not in valid_ipv4_char:
				 raise ValueError("L'indirizzo ipv4 deve contenere solo caratteri numerici")
		 if int(octet) >= 256:
			 raise ValueError("Ogni ottetto di un indirizzo ipv4 non può superare il numero 255")

	 if not isinstance(ipv6_address, str):
		 raise ValueError("L'indirizzo ipv6 deve essere una stringa")
	 if ipv6_address.count("::") > 1:
		 raise ValueError("L'indirizzo IPv6 può contenere al massimo un gruppo vuoto (::)")
	 ipv6_groups = ipv6_address.split(":")
	 if "" in ipv6_groups:
		 index = ipv6_groups.index("")
		 groups_missing = 8 - (len(ipv6_groups) - 1)
		 ipv6_groups = ipv6_groups[:index] + ["0000"]*groups_missing + ipv6_groups[index+1:]
	 if len(ipv6_groups) != 8:
		 raise ValueError("L'indirizzo ipv6 deve essere rappresentato da otto gruppi di caratteri esadecimali")
	 for group in ipv6_groups:
		 for char in group:
			 if char.upper() not in valid_hex_char:
				 raise ValueError("L'indirizzo ipv6 deve contenere solo caratteri esadecimali")
				
				
if __name__ == "__main__":
    host = Host(
        host_name="Host1",
        mac_address="01:23:45:AB:CD:EF",
        ipv4_address="192.168.0.1",
        ipv6_address="2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    )
    print("Host creato con successo!")
   
				 
		 
		 
				 
				 
 		 
		 
