# Simple-websocket-server
Experience the communications between websocket server and client.<br>
Written by [magiclyde](https://magiclyde.me).


# Brief Overview
1. The WebSocket Handshake
2. Exchanging Data Frames
3. Pings and Pongs: The Heartbeat of WebSockets
4. Closing the connection


## Handshake
Serve start on tcp socket, then response encoded header 'Sec-WebSocket-Accept' with incoming client's header 'Sec-WebSocket-Key' and magic string '258EAFA5-E914-47DA-95CA-C5AB0DC85B11' to complete handshake.

## Exchanging Data Frame format

      0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     +-+-+-+-+-------+-+-------------+-------------------------------+
     |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
     |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
     |N|V|V|V|       |S|             |   (if payload len==126/127)   |
     | |1|2|3|       |K|             |                               |
     +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
     |     Extended payload length continued, if payload len == 127  |
     + - - - - - - - - - - - - - - - +-------------------------------+
     |                               |Masking-key, if MASK set to 1  |
     +-------------------------------+-------------------------------+
     | Masking-key (continued)       |          Payload Data         |
     +-------------------------------- - - - - - - - - - - - - - - - +
     :                     Payload Data continued ...                :
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     |                     Payload Data continued ...                |
     +---------------------------------------------------------------+
	
	 ------------------------- explain -------------------------------
	#			#		#
	FIN      		1bit 		tells whether this is the last message in a series. 
						if it's 0, then the server will keep listening for 
						more parts of the message; 
						otherwise, the server should consider the message delivered.

	RSV(1-3)  		1bit each 	have no meaning, default is 0.
	Opcode   		4bit 		defines how to interpret the payload data.
						{ 0x0:CONTINUOUS, 0x1:TEXT, 0x2:BINARY, 0x[3-7]:no meaning, 
						 0x8:CLOSING, 0x9:PING, 0xA:PONG }
								
	Mask     		1bit 		tells whether the message is encoded，should expect this to be 1.
	Payload len  		7bit 		decide when to stop reading.
	Masking-key		1 or 4 bit 	#
	Payload data		x bytes 	#

	------------------------- send and recv-------------------------------
	to do...



# Refer
- [https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers)
- [https://www.websocket.org/aboutwebsocket.html](https://www.websocket.org/aboutwebsocket.html)
- [http://www.jianshu.com/p/eb4c1c724d9e](http://www.jianshu.com/p/eb4c1c724d9e)
