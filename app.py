import socket, time

key = 8194

shutdown = False
join = False

def receving (sock):
	count = 1
	while count != 10:
		if count < 10:
			while True:

				data, addr = sock.recvfrom(64)

				time.sleep(0.2)
				count = count + 1
				return data.decode('utf-8')

		else:
			return " [ NOT ANSWER FROM SERVER ] "

host = socket.gethostbyname(socket.gethostname())
port = 9091

server = ("26.162.211.125", 14900)

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(True)

class client:

	def __init__(self):
		self.admin = 0
		s.sendto(bytes("Create a new app", encoding="UTF-8"), server)

	def setAdmin(self):
		data = ""
		index = ""
		s.sendto(bytes(f"ADMIN, {data}, {index}", encoding="UTF-8"), server)
		r = receving(s)
		if str(r) == "y":
			self.admin = 1
			print(" [ SUCCESFULL ] ")
		else:
			self.admin = 0
			print(" [ NOT SUCCESFULL ] ")

	def request(self, request = None, data = None, index = None):
		s.sendto(bytes(f"PluginRequest, {request}, {data}, {index}", encoding="UTF-8"), server)
		return receving(s)

	def method(self, request = None, data = None):
		s.sendto(bytes(f"PluginMethod, {request}, {data}", encoding="UTF-8"), server)
		return receving(s)

def POST(data = ""):
	s.sendto(bytes(f"POST, {data}", encoding="UTF-8"), server)
	return receving(s)

def GET():
	a = bytes(f"GET", encoding="UTF-8")
	s.sendto(a, server)
	return receving(s)

def PUT(data = "", index = ""):
	s.sendto(bytes(f"PUT, {data}, {index}", encoding="UTF-8"), server)
	return receving(s)

def DELETE(index = ""):
	s.sendto(bytes(f"DELETE, {index}", encoding="UTF-8"), server)
	return receving(s)

def appLIST():
	s.sendto(bytes(f"LIST", encoding="UTF-8"), server)
	return receving(s)

def close():
	s.close()
