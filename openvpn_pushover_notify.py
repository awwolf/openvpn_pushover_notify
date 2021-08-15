TOKEN_VPN="enter here pushover_token"  # pushover token
USER_KEY="enter here pushover_key"  # pushover key

from sys import argv
import http.client, urllib
import time

def send_pushover(message):
    print("Pushover VPN notify: Send Pushover Message: \n" + str(message))
    try:
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                   urllib.parse.urlencode({
                 "token": TOKEN_VPN,
                 "user": USER_KEY,
                 "message": message,
                 "sound": "bike",
               }), {"Content-type": "application/x-www-form-urlencoded"})
        conn.getresponse()
    except:
        print("Pushover VPN notify: Can not send message")


def load_file():
    if len(argv) >= 2:
        filename = argv[1]
    else:
        filename = "/etc/openvpn/openvpn-status.log"
    f = open(filename,"r")
    data = []
    for i in f.readlines():
        i = i.replace("\n","")
        data.append(i)
    f.close()
    return data

def find_in_data(data, strline):
    for idx, i in enumerate(data):
        if i[:len(strline)] == strline:
            return idx

old_clients = set()
clients = set()


while(True):
    data = load_file()
    updated = data[1]
    clients_list = {}
    clients = set()
    sta_routing_table = find_in_data(data, "ROUTING TABLE")
    for i in range(3,sta_routing_table):
        j = data[i].split(",")
        clients_list[j[0]] = j[1:]
        clients.add(j[0])

    clients = clients - {'UNDEF'}
    c_in = clients.difference(old_clients)
    c_out = old_clients.difference(clients)

    if len(c_in) > 0:
        message = "Client Connected to VPN:\n"
        for i in c_in: message = message + str(i) + "\n"
        send_pushover(message)
    if len(c_out) > 0:
        message = "Client Disconnected from VPN:\n"
        for i in c_out: message = message + str(i) + "\n"
        send_pushover(message)

    old_clients = clients
    time.sleep(1)


