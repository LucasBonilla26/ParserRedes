import networkx as nx
import os
import ipaddress
from faker import Faker
import shutil

def write_startupIP(name,eth,ip):
    file = open(name.lower().replace(" ", "") + ".startup", "a")
    file.write("ifconfig eth" + str(eth) + " " + str(ip) + "/24 up\n") #str(eth)
    file.close()

def generate_ip():
    ex = Faker()
    return ipaddress.IPv4Address(ex.ipv4())

def create_quagga(name,ip):
    os.makedirs(str(name).lower().replace(" ", "") + '/etc/quagga', exist_ok=True)

    file = open(str(name).lower().replace(" ", "") + '/etc/quagga/daemons', "a")
    file.write("zebra=yes\nbgpd=no\nospfd=no\nospf6d=no\nripd=yes\nripngd=no")
    file.close()

    file = open(str(name).lower().replace(" ", "") + '/etc/quagga/zebra.conf', "a")
    file.write("! -*- zebra -*-\n!\n! zebra configuration file\n!\nhostname r1\npassword zebra\nenable password zebra\n!\n! Static default route sample.\n!ip route 0.0.0.0/0 203.181.89.241\n!\nlog file /var/log/quagga/zebra.log")
    file.close()

    file = open(str(name).lower().replace(" ", "") + '/etc/quagga/ripd.conf',"a")
    file.write("!\nhostname ripd\npassword zebra\nenable password zebra\n!\nrouter rip\nredistribute connected\nnetwork " + str(ip) + "/24\n!\nlog file /var/log/quagga/ripd.log")
    file.close()

if __name__ == '__main__':
    G = nx.read_gml('Renam.gml')
    print(len(G.nodes()))

    appear = {}
    file = open("lab.conf", "a")
    i = 1

    #each edge is a network
    for u, v in G.edges:

        # generate net
        ip = generate_ip()
        #Check if the nodes already have an ip
        if u not in appear:
            appear.update({str(u):0})
            create_quagga(u,ip)
        else:
            appear[str(u)] = appear[str(u)] + 1

        if v not in appear:
            appear.update({str(v):0})
            create_quagga(v,ip)
        else:
            appear[str(v)] = appear[str(v)] + 1

        #labconf
        file.write(str(u).lower().replace(" ", "") + "[" + str(appear[str(u)]) + "]=" + str(i) + "\n")
        file.write(str(v).lower().replace(" ", "") + "[" + str(appear[str(v)]) + "]="+ str(i) + "\n")
        i+=1
        
        write_startupIP(u,appear[str(u)],ip+1)
        write_startupIP(v,appear[str(v)],ipaddress.IPv4Address(ip+2))

    print(appear)


