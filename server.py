import socket, time, os
import Plugin

host = socket.gethostbyname(socket.gethostname())
port = 14900

clients = []

data_server = []
admins = []
whitelist = []
blacklist = []

whitelist_eneable = True

log = False

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))

a = input("Loging? [Y/n]")
if a == "y" or a == "Y" or a == "д"  or a == "Д":
	log = True
else:
	log = False

a = input("Enable white list? [Y/n]")
if a == "y" or a == "Y" or a == "д"  or a == "Д":
	whitelist_eneable = True
else:
	whitelist_enable = False
a = 0

quit = False
print(f"[ Server Started on {host}:{port} ]")

while not quit:
	if not quit:
		try:
			data, addr = s.recvfrom(1024)

			if addr not in clients:
				clients.append(addr)

			data0 = str(data).split("'")
			data0.pop(0)
			data0 = " ".join(data0)
			data0 = str(data0).split(",")

			itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

			a = 0

			if data0[0] == "PluginRequest":
				for x in admins:
					if x == addr:
						if log:
							print("[PluginRequest]=["+str(addr[1])+"]=["+itsatime+"] ::  ",end="")
							print(data.decode("utf-8"))
						s.sendto(bytes(Plugin.request(data[1], data0[2], data0[3]), encoding="UTF-8"), addr)
						a = 1

				if a == 0:
					s.sendto(bytes(" [ YOU ARE NOT ADMIN ] ",encoding="UTF-8"), addr)

			elif data0[0] == "PluginMethod":
				for x in admins:
					if x == addr:
						if log:
							print("[PluginMethod]=["+str(addr[1])+"]=["+itsatime+"] ::  ",end="")
							print(data.decode("utf-8"))
						s.sendto(bytes(Plugin.method(data[1], data0[2]), encoding="UTF-8"), addr)
						a = 1

				if a == 0:
					s.sendto(bytes(" [ YOU ARE NOT ADMIN ] ",encoding="UTF-8"), addr)
			
			else:
				if data0[0] != "ADMIN":
					print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"] ::  ",end="")
					print(data.decode("utf-8"))

				if data0[0] == "ADMIN":
					a = input("Set admin? [Y/n]")
					if a == "y" or a == "Y" or a == "д"  or a == "Д":
						admins.append(addr)
						s.sendto(bytes("y", encoding="UTF-8"), addr)
					else:
						s.sendto(bytes("n", encoding="UTF-8"), addr)

				a = 0

				if data0[0] == "POST":
					for x in admins:
						if x == addr:
							data_server.append(data0[1])
							s.sendto(bytes(" [ SUCCESFUL ] ",encoding="UTF-8"), addr)
							print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"] :: ",end="")
							print(" ADD DATA TO YOUR SERVER ")
							a = 1
					
					if a == 0:
						s.sendto(bytes(" [ YOU ARE NOT ADMIN ] ",encoding="UTF-8"), addr)
				
				elif data0[0] == "GET":
					a = ",".join(map(str, data_server))
					s.sendto(bytes(data_server ,encoding="UTF-8"), addr)
					print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"] :: ",end="")
					print(" READ DATA WITH YOUR SERVER ")

				elif data0[0] == "PUT":
					for x in admins:
						if x == addr:
							data_server[int(data0[2])] == data0[1]
							s.sendto(bytes(" [ SUCCESFUL ] ",encoding="UTF-8"), addr)
							print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"] :: ",end="")
							print(" EDIT DATA IN YOUR SERVER ")
							a = 1
					
					if a == 0:
						s.sendto(bytes(" [ YOU ARE NOT ADMIN ] ",encoding="UTF-8"), addr)

				elif data0[0] == "DELETE":
					for x in admins:
						if x == addr:
							data_server.pop(int(data0[1]))
							s.sendto(bytes(" [ SUCCESFUL ] ", encoding="UTF-8"), addr)
							print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"] :: ",end="")
							print(" DELETE DATA WITH YOUR SERVER ")
							a = 1
					
					if a == 0:
						s.sendto(bytes(" [ YOU ARE NOT ADMIN ] ",encoding="UTF-8"), addr)

				elif data0[0] == "LIST":
					for x in admins:
						if x == addr:
							data_server.pop(int(data0[2]))
							s.sendto(bytes(clients, encoding="UTF-8"), addr)
							print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"] :: ",end="")
							print(" GET CLIENT LIST WITH YOUR SERVER ")
							a = 1
					
					if a == 0:
						s.sendto(bytes(" [ YOU ARE NOT ADMIN ] ",encoding="UTF-8"), addr)
			
		except KeyboardInterrupt:
			print("[ SERVER STOPED ]")
			exit()
			s.close()

s.close()