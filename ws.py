#coding: utf-8
import socket, threading, hashlib, base64, struct, array, os

def maskHandle(key, data):
	'''
	see https://docs.python.org/2/library/array.html
	'''
	_m = array.array("B", key)
	_d = array.array("B", data)
	for i in xrange(len(_d)):
		_d[i] ^= _m[i % 4]
	return _d.tostring()

def recvDataFrame(sock):
	# read 2 bytes, 16 bit
	bytes_1_2 = sock.recv(2)

	# fin ~ opcode
	byte_1 = ord(bytes_1_2[0]) 
	
	# mask ~ payload len
	byte_2 = ord(bytes_1_2[1]) 

	# get highest bit in first byte
	fin = byte_1 >> 7 & 1 

	# get last 4 bit in first byte
	opcode = byte_1 & 0xf
	if opcode == 0x8:
		print '\nconnection closed.\n'
		return fin, opcode, ''

	# get highest bit in second byte
	is_mask = byte_2 >> 7 & 1

	# # get last 7 bit in second byte
	payload_len = byte_2 & 0x7f

	# Decoding Payload Length
	if payload_len == 0x7e:
		# Read the next 16 bits and interpret those as an unsigned integer. You're done.
		next_bytes = sock.recv(2)
		payload_len = struct.unpack("!H", next_bytes)[0]
	elif payload_len == 0x7f:
		# Read the next 64 bits and interpret those as an unsigned integer. You're done.
		next_bytes = sock.recv(8)
		payload_len = struct.unpack("!H", next_bytes)[0]
	else:
		pass

	# If the MASK bit was set (and it should be, for client-to-server messages), 
	# read the next 4 octets (32 bits); this is the masking key
	if is_mask:
		mask_key = sock.recv(4)
		# then Reading and Unmasking the Data from client
		payload = sock.recv(payload_len)
		return fin, opcode, maskHandle(mask_key, payload)

def sendDataFrame(sock, data):
	fin = True
	is_mask = False
	byte_1 = opcode = 0x01

	# it is the last message if fin =1
	if fin:
		byte_1 = byte_1 | 0x80

	frame_data = struct.pack('B',byte_1)
	
	length = len(data)
	
	byte_2 = 0
	if is_mask:
		byte_2 = 0x80

	if length < 126:
		frame_data += struct.pack('B',byte_2|length)
	elif length <= 0xFFFF:
		frame_data += struct.pack('!BH',byte_2|126,length)
	else:
		frame_data += struct.pack('!BQ',byte_2|127,length)

	# not trigger when send data...
	if is_mask:
		mask = os.urandom(4)
		data = mask + maskHandle(mask, data)

	frame_data += data
	sock.send(frame_data)
	return len(frame_data)

def getHeaders(sock):
	while True:
		data = sock.recv(1024)
		if not data or len(data) < 1024:
			break
	
	headers = {}
	for header in data.split('\r\n'):
		item = header.split(':', 2)
		if len(item) < 2:
			continue
		headers[item[0]] = item[1].strip()

	return headers

def handShake(sock):
	headers = getHeaders(sock)

	if 'Sec-WebSocket-Key' not in headers:
		sock.send('HTTP/1.1 400 Bad Request\r\n'+'Sec-WebSocket-Key not found\r\n\r\n')
		sock.close()
		return False

	# response header: Sec-WebSocket-Accept
	key = headers['Sec-WebSocket-Key']
	sha1 = hashlib.sha1()
	sha1.update(key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
	accept_val = base64.b64encode(sha1.digest())

	response = ('HTTP/1.1 101 Switching Protocols\r\n'
		'Upgrade:websocket\r\n'
		'Connection:Upgrade\r\n'
		'Sec-WebSocket-Accept:%s\r\n'
		'\r\n' % accept_val)
	sock.send(response)
	return True

def webSocketLink(sock, addr):
	if not handShake(sock):
		return False

	# handshake completed. switch from HTTP to WebSocket & communicate...
	print 'Accept new web socket from %s:%s...' % addr

	while True:
		fin, opcode, data = recvDataFrame(sock)
		if opcode == 0x8:
			sock.close()
			break
		else:
			print 'recv data:\t', data
			send_data = 'Server recv:' + data
			# response data frame
			sendDataFrame(sock, send_data)

def main():
	HOST, PORT = '', 8282
	REQUEST_MAX_CONN = 5

	# serve on tcp socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(REQUEST_MAX_CONN)
	print 'Serve start on port %d' % PORT

	while True:
		sock, addr = s.accept()
		t = threading.Thread(target = webSocketLink, args = (sock, addr))
		t.start()

if __name__ == '__main__':
	main()
