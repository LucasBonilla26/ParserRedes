import networkx as nx
import os
import ipaddress
from faker import Faker
import shutil

def write_startupIP(name,eth,ip):
    file = open("D:\Master\TPC\practica2\PA_" + name.strip() + ".startup", "a")
    file.write("ifconfig eth" + str(eth) + " " + str(ip) + "/24 up\n") #str(eth)
    file.close()

def generate_ip():
    ex = Faker()
    return ipaddress.IPv4Address(ex.ipv4())


G = nx.read_gml('D:\Master\TPC\practica2\Renam.gml')
print(G.edges)

appear = {}
file = open("D:\Master\TPC\practica2\lab.conf", "a")
i = 1
#each edge is a network
for u, v in G.edges:
    
    #Check if the nodes already have an ip
    if u not in appear:
        appear.update({str(u):0})
    else:
        appear[str(u)] = appear[str(u)] + 1

    if v not in appear:
        appear.update({str(v):0})
    else:
        appear[str(v)] = appear[str(v)] + 1

    #labconf
    file.write("PA_" + str(u).strip() + "[" + str(appear[str(u)]) + "]=" + str(i) + "\n")
    file.write("PA_" + str(v).strip() + "[" + str(appear[str(v)]) + "]="+ str(i) + "\n")
    i+=1
    
    ip = generate_ip()
    write_startupIP(u,appear[str(u)],ip)
    write_startupIP(v,appear[str(v)],ipaddress.IPv4Address(ip+1))


print(appear)


