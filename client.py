# import socket
# import hashlib
# import struct

# ipAddress = "127.0.0.1"
# port = 1337
# responsePort = 1338
# timeOut = 2

# sendingData = ["Pakistan","nausherwan","k200428","sethabde","20k0122"]
# dataUnpacker = struct.Struct('I I 8s 32s')
# responseUnpacker = struct.Struct('I I 32s')

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ACK = 0
# SEQ = 0

# for data in sendingData:
#     print("Sending Data: {0}".format(data))

#     # convert this item into bytes (for transmission)
#     byteData = data.encode()

#     # Create a Checksum for this Data
#     values = (ACK, SEQ, byteData)
#     checksumPacker = struct.Struct('I I 8s')

#     checksumConverted = (checksumPacker.pack(*values))
#     checksum = bytes(hashlib.md5(
#         checksumConverted).hexdigest(), encoding="UTF-8")

#     # prepare a packet for sending
#     values = (ACK, SEQ, byteData, checksum)
#     thisPacket = dataUnpacker.pack(*values)

#     print("Sending packets...")
#     done = False
#     while done == False:
#         try:
#             currentACK = ACK
#             sock.sendto(thisPacket, (ipAddress, port))
#             print("Packet sent!")

#             # Wait for the server's response
#             responseSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             responseSocket.settimeout(timeOut)
#             responseSocket.bind((ipAddress, responsePort))

#             print("Waiting for the Server's Response...")

#             # Listen and get data from the server
#             receivedData, addr = responseSocket.recvfrom(1024)
#             receivedPacket = responseUnpacker.unpack(receivedData)

#             # Check if the ACK was corrupted
#             receivedACK = receivedPacket[0]
#             if currentACK != receivedACK:
#                 # Display the received packet's info
#                 print("The Server's Response: ")
#                 print("ACK:", receivedPacket[0])
#                 print("SEQ:", receivedPacket[1])
#                 print("Data:", receivedPacket[2])
#                 print()
#                 print("[INFO] The data was corrupted!")
#                 continue
#             else:
#                 # Display the received packet's info
#                 print("The Server's Response: ")
#                 print("ACK:", receivedPacket[0])
#                 print("SEQ:", receivedPacket[1])
#                 print("Data:", receivedPacket[2])
#                 print()
#                 print("[INFO] The data was not corrupted")
#                 correctRespSequence = receivedPacket[1]
#                 break
#             done = True
#         # If the timeout occured, throw an exception and resend the packet
#         except socket.timeout:
#             done = False
#             print("[INFO] Timeout occured while waiting for the server's response.")
#             print("##############################################################")
#             continue

#     # update the sequence number
#     SEQ = correctRespSequence
#     # flip the ACK
#     if ACK == 0:
#         ACK = 1
#     else:
#         ACK = 0

#     print("#######################################################################")

# sock.close()
# responseSocket.close()
