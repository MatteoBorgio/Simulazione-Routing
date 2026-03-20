import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ip_verification_module import verify_ipv4_address
from enum import Enum
from random import randint

class State(Enum):
	CLOSED = "CLOSED"
	LISTEN = "LISTEN"
	SYN_SENT = "SYN_SENT"
	SYN_RECEIVED = "SYN RECEIVED"
	ESTABLISHED = "ESTABLISHED"
	FIN_WAIT = "FIN_WAIT"	
	CLOSE_WAIT = "CLOSE WAIT"
	
class TCPSession:
	def __init__(self, host: "Host", target_ip: str, target_port: int, source_port: int):
		
		target_ip_validation = verify_ipv4_address(target_ip)
		if target_ip_validation["success"] == False:
			raise ValueError(target_ip_validation["error"])
		
		if not isinstance(target_port) or not isinstance(source_port):
			raise ValueError("La porta deve essere un intero")
		
		self.target_ip = target_ip
		self.target_port = target_port
		self.source_port = source_port
		self.state = State.CLOSED		
		my_sequence_number = randint(1, 1000)
		expected_ack_num = 0
		transmission_buffer = {}
		reception_buffer = {}
		
