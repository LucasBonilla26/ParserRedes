import networkx as nx
import os
import ipaddress
from faker import Faker
import shutil

def write_startupIP(name,eth,ip):
    file = open(name.lower().replace(" ", "") + ".startup", "a")
    file.write("ifconfig eth" + str(eth) + " " + str(ip) + "/30 up\n") #str(eth)
    file.close()

def create_quagga(name,ip):
    os.makedirs(str(name).lower().replace(" ", "") + '/etc/quagga', exist_ok=True)

    file = open(str(name).lower().replace(" ", "") + '/etc/quagga/daemons', "a")
    file.write("zebra=yes\nbgpd=no\nospfd=no\nospf6d=no\nripd=yes\nripngd=no")
    file.close()

    file = open(str(name).lower().replace(" ", "") + '/etc/quagga/zebra.conf', "a")
    file.write("! -*- zebra -*-\n!\n! zebra configuration file\n!\nhostname r1\npassword zebra\nenable password zebra\n!\n! Static default route sample.\n!ip route 0.0.0.0/0 203.181.89.241\n!\nlog file /var/log/quagga/zebra.log")
    file.close()

    file = open(str(name).lower().replace(" ", "") + '/etc/quagga/ripd.conf',"a")
    file.write("!\nhostname ripd\npassword zebra\nenable password zebra\n!\nrouter rip\nredistribute connected\nnetwork " + str(ip) + "/16\n!\nlog file /var/log/quagga/ripd.log")
    file.close()

    file = open(name.lower().replace(" ", "") + ".startup", "a")
    file.write("/etc/init.d/quagga start\n")
    file.close()

if __name__ == '__main__':
    G = nx.read_gml('Renam.gml')
    print(len(G.nodes()))

    appear = {}
    file = open("lab.conf", "a")
    i = 1

    # generate net 100.1.XXXXXXXX.XXXXXXXX/16 100.1.0.000000XX/30 +4 por red
    ip = global_ip= ipaddress.IPv4Address("100.1.0.0")

    #each edge is a network
    for u, v in G.edges:
        
        ip+=4
        #Check if the nodes already have an ip
        if u not in appear:
            appear.update({str(u):0})
            create_quagga(u,global_ip)
        else:
            appear[str(u)] = appear[str(u)] + 1

        if v not in appear:
            appear.update({str(v):0})
            create_quagga(v,global_ip)
        else:
            appear[str(v)] = appear[str(v)] + 1

        #labconf
        file.write(str(u).lower().replace(" ", "") + "[" + str(appear[str(u)]) + "]=" + str(i) + "\n")
        file.write(str(v).lower().replace(" ", "") + "[" + str(appear[str(v)]) + "]="+ str(i) + "\n")
        i+=1
        
        write_startupIP(u,appear[str(u)],ip+1)
        write_startupIP(v,appear[str(v)],ipaddress.IPv4Address(ip+2))

    print(appear)


