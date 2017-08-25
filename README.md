# Simple-websocket-server
Experience the communications between websocket server and client.<br>
Written by [magiclyde](https://magiclyde.me).


# Brief Overview
1. The WebSocket Handshake
2. Exchanging Data Frames


## Handshake
Serve start on tcp socket, then response encoded header '**Sec-WebSocket-Accept**' with incoming client's header '**Sec-WebSocket-Key**' and magic string '258EAFA5-E914-47DA-95CA-C5AB0DC85B11' to complete handshake.


## Exchanging Data

### Frame Format

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
    
     #            #          #
     FIN          1 bit      tells whether this is the last message in a series.               
                             if it's 0, then the server will keep listening for                
                             more parts of the message;                                        
                             otherwise, the server should consider the message delivered.      
     RSV(1-3)     1 bit each have no meaning, default is 0.                                    
     Opcode       4 bit      defines how to interpret the payload data.                        
                             { 0x0:CONTINUOUS, 0x1:TEXT, 0x2:BINARY, 0x[3-7]:no meaning,       
                               0x8:CLOSING, 0x9:PING, 0xA:PONG }                               
     Mask         1 bit      tells whether the message is encoded，should expect this to be 1. 
     Payload len  7 bit      decide when to stop reading.                                      
     Masking-key  1 or 4 bit ...                                                                 
     Payload data x bit      ...                                                               



### Recv Data Frame
1. Decoding Payload Length
2. Reading and Unmasking the payload data from client

### Send Data Frame
send frame + data


# Refer
- [https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers)
- [https://www.websocket.org/aboutwebsocket.html](https://www.websocket.org/aboutwebsocket.html)
- [http://liyumeng.me/detail/3](http://liyumeng.me/detail/3)
