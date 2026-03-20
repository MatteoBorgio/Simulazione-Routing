import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ip_verification_module import verify_mac_address, verify_ipv4_address, verify_ipv6_address
from utils.lan_verification_module import verify_if_is_in_the_same_lan
from simulation.packet import Packet, ArpRequest
from simulation.ethernet_frame import EthernetFrame

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
		if ipv6_validation["success"] == False:
			raise ValueError(ipv6_validation["error"])
			
		default_gateway_validation = verify_ipv4_address(default_gateway)
		if default_gateway_validation["success"] == False:
			raise ValueError(default_gateway_validation["error"])
		elif default_gateway == ipv4_address:
			raise ValueError("Il default gateway deve essere diverso dall'indirizzo ip del dispositivo.")
					
		self.name = name
		self.mac_address = mac_address
		self.ipv4_address = ipv4_address
		self.ipv6_address = ipv6_address
		self.default_gateway = default_gateway
		self.connected_switch = None
		self.packet_buffer = []
		
		self.subnet_mask = self.calculate_subnet_mask(self.ipv4_address)
		self.arp_table = {}
		self.routing_table = {}
	
	def calculate_subnet_mask(self, ipv4_address: str) -> str:
		ipv4_octets = ipv4_address.split(".")
		if int(ipv4_octets[0]) <= 127:
			return "255.0.0.0"
		elif int(ipv4_octets[0]) > 127 and int(ipv4_octets[0]) <=191:
			return "255.255.0.0"
		else:
			return "255.255.255.0"
			
	def populate_arp_table(self, device) -> None:
		try:
			ipv4_address = device.ipv4_address
			mac_address = device.mac_address
			
			self.arp_table[ipv4_address] = mac_address 
		except AttributeError as e:
			raise ValueError(f"Dispositivo non valido. Manca l'attributo: {e}")
			
	def populate_routing_table(self, device) -> None:
		try:
			ipv4_address = device.ipv4_address
			subnet_mask = device.subnet_mask
			
			if verify_if_is_in_the_same_lan(self.ipv4_address, self.subnet_mask, ipv4_address):
				self.routing_table[ipv4_address] = {"Destination": ipv4_address, "Netmask": subnet_mask, "Gateway": "0.0.0.0"}
			else:				
				self.routing_table[ipv4_address] = {"Destination": ipv4_address, "Netmask": subnet_mask, "Gateway": self.default_gateway}
		except AttributeError as e:
			raise ValueError(f"Impossibile calcolare il routing. Manca l'attributo: {e}")
			
			
	def create_frame(self, content_payload: Packet, destination_mac_address="FF:FF:FF:FF:FF:FF") -> EthernetFrame:
		return EthernetFrame(self, destination_mac_address, content_payload)
		
	def receive(self, frame: EthernetFrame) -> None:
		try:
			if frame.destination_mac_address != self.mac_address and frame.destination_mac_address != "FF:FF:FF:FF:FF:FF":
				return
				
			payload = frame.content_payload
			
			if payload.destination_ip != self.ipv4_address:
				return
				
			self.arp_table[payload.source_ip] = payload.source_mac
			
			if payload.content_payload == "ARP WHO HAS":
				arp_reply = ArpRequest(self.ipv4_address, self.mac_address, payload.source_ip, "ARP IS AT")
				reply_frame = self.create_frame(arp_reply, payload.source_mac)
				self.connected_switch.receive_frame(reply_frame)
				return
			
			if payload.content_payload == "ARP IS AT": 
				self.arp_table[payload.source_ip] = payload.source_mac
				
				packet_to_send = []
				packet_not_to_send = []
				
				for target, packet in self.packet_buffer:
					if target == payload.source_ip:
						packet_to_send.append((target, packet))
					else:
						packet_not_to_send.append((target, packet))
						
				self.packet_buffer = packet_not_to_send
				
				for target, packet in packet_to_send:
					self.connected_switch.receive_frame(EthernetFrame(self, payload.source_mac, packet))
				
				return
				
			if payload.protocol.lower() == "udp":
				print(f"Ricevuto: {payload}")
				return
			
			if payload.protocol.lower() == "tcp":
				pass
		
						
		except AttributeError as e:
			raise ValueError(f"Impossibile calcolare il routing. Manca l'attributo: {e}")
	
	def send_packet(self, destination_ipv4: str, payload: Packet, protocol: str) -> None:
		if not isinstance(protocol, str):
			raise ValueError("Protocollo non valido")
			
		if protocol.lower() not in ["udp", "tcp"]:
			raise ValueError("Protocollo non valido")
			
		if self.connected_switch is None:
			raise ValueError("Impossibile inoltrare la richiesta")
			
		is_in_same_lan = verify_if_is_in_the_same_lan(self.ipv4_address, self.subnet_mask, destination_ipv4)
		
		target_ip = destination_ipv4 if is_in_same_lan else self.default_gateway
		
		if target_ip in self.arp_table:
			destination_mac_address = self.arp_table[target_ip]
			frame = self.create_frame(payload, destination_mac_address)
			self.connected_switch.receive_frame(frame)
		else:
			self.packet_buffer.append((target_ip, payload))
			arp_request = ArpRequest(self.ipv4_address, self.mac_address, target_ip, "ARP WHO HAS")
			broadcast_frame = self.create_frame(arp_request, "FF:FF:FF:FF:FF:FF")
			self.connected_switch.receive_frame(broadcast_frame)
			return
			
		# TCP and UDP packets sending procedure not implemented
	
	def __str__(self):
		return f"Host: {self.name}\nMac: {self.mac_address}\nIpv4: {self.ipv4_address}\nIpv6: {self.ipv6_address}\nGateway: {self.default_gateway}\nSubnet: {self.subnet_mask}"
			
			
			
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
