import networkx as nx
import os
import ipaddress
from faker import Faker
import shutil

def write_startupIP(name,eth,ip):
    file = open("kathara/pc" + str(name) + ".startup", "a")
    file.write("ifconfig eth" + str(eth) + " " + str(ip) + "/30 up\n") #str(eth)
    file.close()

def create_quagga(name,ip):
    os.makedirs("kathara/pc" + str(name) + '/etc/quagga', exist_ok=True)

    file = open("kathara/pc" + str(name) + '/etc/quagga/daemons', "a")
    file.write("zebra=yes\nbgpd=no\nospfd=no\nospf6d=no\nripd=yes\nripngd=no")
    file.close()

    file = open("kathara/pc" + str(name) + '/etc/quagga/zebra.conf', "a")
    file.write("! -*- zebra -*-\n!\n! zebra configuration file\n!\nhostname r1\npassword zebra\nenable password zebra\n!\n! Static default route sample.\n!ip route 0.0.0.0/0 203.181.89.241\n!\nlog file /var/log/quagga/zebra.log")
    file.close()

    file = open("kathara/pc" + str(name) + '/etc/quagga/ripd.conf',"a")
    file.write("!\nhostname ripd\npassword zebra\nenable password zebra\n!\nrouter rip\nredistribute connected\nnetwork " + str(ip) + "/16\n!\nlog file /var/log/quagga/ripd.log")
    file.close()

    file = open("kathara/pc" + str(name) + ".startup", "a")
    file.write("/etc/init.d/quagga start\n")
    file.close()

if __name__ == '__main__':

    # If the gml file is a multigraph you have to write multigraph 1 in graph []
    G = nx.read_gml('Rediris.gml',label='id')
    appear = {}

    os.makedirs("kathara", exist_ok=True)
    file = open("kathara/lab.conf", "a")
    i = 1

    # generate net 100.1.XXXXXXXX.XXXXXXXX/16 100.1.0.000000XX/30 +4 por red
    ip = global_ip= ipaddress.IPv4Address("100.1.0.0")

    #each edge is a network
    for u, v in list(G.edges()):

        ip+=4

        #Check if the nodes already have an ip
        if u not in appear:
            appear.update({u:0})
            create_quagga(u,global_ip)
        else:
            appear[u] += 1

        if v not in appear:
            appear.update({v:0})
            create_quagga(v,global_ip)
        else:
            appear[v] += 1

        #labconf
        file.write("pc" + str(u) + "[" + str(appear[u]) + "]=" + str(i) + "\n")
        file.write("pc" + str(v) + "[" + str(appear[v]) + "]="+ str(i) + "\n")
        i+=1
        
        write_startupIP(u,appear[u],ip+1)
        write_startupIP(v,appear[v],ip+2)


