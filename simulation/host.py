import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ip_verification_module import verify_mac_address, verify_ipv4_address, verify_ipv6_address
from utils.lan_verification_module import verify_if_is_in_the_same_lan
from simulation.packet import Packet

class Host:
	def __init__(self, name: str, mac_address: str, ipv4_address: str, ipv6_address: str, default_gateway: str):
		self.valid_hex_char = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
		if not isinstance(name, str):
			raise ValueError("L'identificativo dell'host deve essere una stringa.")
		
		mac_address_validation = verify_mac_address(mac_address)
		if mac_address_validation["success"] == False:
			raise ValueError(mac_address_validation["error"])
		
		ipv4_validation = verify_ipv4_address(ipv4_address)
		if ipv4_validation["success"] == False:
			raise ValueError(ipv4_validation["error"])
		
		ipv6_validation = verify_ipv6_address(ipv6_address)
		if ipv4_validation["success"] == False:
			raise ValueError(ipv4_validation["error"])
			
		default_gateway_validation = verify_ipv4_address(default_gateway)
		if default_gateway_validation["success"] == False:
			raise ValueError(default_gateway["error"])
		elif default_gateway == ipv4_address:
			raise ValueError("Il default gateway deve essere diverso dall'indirizzo ip del dispositivo.")
					
		self.name = name
		self.mac_address = mac_address
		self.ipv4_address = ipv4_address
		self.ipv6_address = ipv6_address
		self.default_gateway = default_gateway
		
		self.subnet_mask = self.calculate_subnet_mask(self.ipv4_address)
		self.arp_table = {}
		self.routing_table = {}

	def calculate_subnet_mask(self, ipv4_address: str) -> str:
		ipv4_octets = ipv4_address.split(".")
		if int(ipv4_octets[0]) <= 127:
			return "255.0.0.0"
		elif int(ipv4_address[0]) > 127 and int(ipv4_address[0]) <=191:
			return "255.255.0.0"
		else:
			return "255.255.255.0"
			
	def populate_arp_table(self, device):
		try:
			name = device.name
			ipv4_address = device.ipv4_address
			mac_address = device.mac_address
			
			self.arp_table[name] = {"Ipv4": ipv4_address, "Mac": mac_address}
		except AttributeError as e:
			raise ValueError(f"Dispositivo non valido. Manca l'attributo: {e}")
			
	def populate_routing_table(self, device):
		try:
			name = device.name
			ipv4_address = device.ipv4_address
			subnet_mask = device.subnet_mask
			
			if verify_if_is_in_the_same_lan(self.ipv4_address, self.subnet_mask, ipv4_address):
				self.routing_table[name] = {"Destination": ipv4_address, "Netmask": subnet_mask, "Gateway": "0.0.0.0"}
			else:				
				self.routing_table[name] = {"Destination": ipv4_address, "Netmask": subnet_mask, "Gateway": ipv4_address}
		except AttributeError as e:
			raise ValueError(f"Impossibile calcolare il routing. Manca l'attributo: {e}")
			
# --- CODICE DI PROVA ---
if __name__ == "__main__":
	print("=== TEST CREAZIONE HOST ===")
	try:
		# 1. Creiamo il nostro host principale
		my_host = Host(
			name="PC-Principale",
			mac_address="AA:BB:CC:DD:EE:FF",
			ipv4_address="192.168.1.10",
			ipv6_address="2001:0db8:85a3:0000:0000:8a2e:0370:7334",
			default_gateway="192.168.1.1"
		)
		print(f"Host '{my_host.name}' creato con successo.")
		print(f"IP: {my_host.ipv4_address} | Mask: {my_host.subnet_mask}")
		print("-" * 30)
		# 2. Creiamo altri due host per testare ARP e Routing
		# Uno nella stessa LAN (192.168.1.x)
		host_locale = Host("Stampante", "00:11:22:33:44:55", "192.168.1.50", "::1", "192.168.1.1")
		# Uno in una LAN differente (10.0.0.x)
		host_remoto = Host("Server-Web", "FF:EE:DD:CC:BB:AA", "10.0.0.1", "::1", "10.0.0.254")
		# 3. Test Popolamento Tabelle
		print("=== TEST ARP & ROUTING ===")
		# Aggiungiamo i dispositivi
		for dev in [host_locale, host_remoto]:
			my_host.populate_arp_table(dev)
			my_host.populate_routing_table(dev)
			print(f"Inserito dispositivo: {dev.name} ({dev.ipv4_address})")
		# 4. Visualizzazione Risultati
		print("\n--- ARP TABLE ---")
		for target, data in my_host.arp_table.items():
			print(f"{target} -> IP: {data['Ipv4']}, MAC: {data['Mac']}")
		print("\n--- ROUTING TABLE ---")
		for target, data in my_host.routing_table.items():
			print(f"Verso {target}: Dest: {data['Destination']}, GW: {data['Gateway']}")
			if data['Gateway'] == "0.0.0.0":
				print("   [Stato: Connessione Diretta / LAN]")
			else:
				print(f"   [Stato: Inoltro tramite Gateway {data['Gateway']}]")
	except Exception as e:
		print(f"ERRORE DURANTE IL TEST: {e}")
