import scapy.all as scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answer_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    clients_list = []
    for element in answer_list:
        client_dict = {'IP': element[1].psrc, 'MAC': element[1].hwsrc}
        clients_list.append(client_dict)
    return (clients_list)

def print_result(result_list):
    print('IP\t\t\tMAC address\n>----------------------------------------<')
    for client in result_list:
        print(client['IP'] + '\t\t' + client['MAC'])

scan_result = scan('192.168.1.1/24')
print_result(scan_result)