#coding: utf-8
import socket, time, threading, hashlib, base64

'''
@see https://www.websocket.org/aboutwebsocket.html
'''

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

def webSocketLink(sock, addr):
	headers = getHeaders(sock)

	if 'Sec-WebSocket-Key' not in headers:
		return False

	print 'Accept new web socket from %s:%s...' % addr
	key = headers['Sec-WebSocket-Key']
	sha1 = hashlib.sha1()
	sha1.update(key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
	accept_val = base64.b64encode(sha1.digest())

	response = ('HTTP/1.1 101 Switching Protocols\r\n'
		'Upgrate:Websocket\r\n'
		'Connection:Upgrate\r\n'
		'Sec-WebSocket-Accept:%s\r\n'
		'\r\n' % accept_val)
	sock.send(response)
	# http handshake end.

	# switch from HTTP to WebSocket
	while True:
		time.sleep(1)



HOST, PORT = '', 8282
REQUEST_MAX_CONN = 5

# serve on tcp socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(REQUEST_MAX_CONN)

while True:
	sock, addr = s.accept()
	t = threading.Thread(target = webSocketLink, args = (sock, addr))
	t.start()