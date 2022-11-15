import subprocess # Correr comandos con python 
import optparse # Crear comandos 
import re # Expresiones regulares

# Obtener argumentos
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest = 'interface', help = 'Interface para cambiar direccion MAC')
    parser.add_option('-m', '--mac', dest = 'new_mac', help = 'Nueva dirección MAC')

    # Guardar las opciones interface, new_mac y los argumentos --interface --mac    
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error('[-] Por favor indicar una interfaz, usa --help para mas informacón')
    elif not options.new_mac:
        parser.error('[-] Por favor indicar una Direeción MAC, usa --help para mas informacón')
    return options

# Crear comandos con python
def change_mac(interface, new_mac):
    print(f'[+] Cambiando dirección MAC para la interfaz: {interface} a {new_mac}')
    subprocess.call(['ifconfig', interface, 'down']) # Apagar interfaz de red
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac]) # Cambiar MAC de la interfaz hw(hardware)
    subprocess.call(['ifconfig', interface, 'up'])

# Obtener dirección MAC actual
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface]) 
    mac_addres_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_addres_result:
        return mac_addres_result.group(0)
    else:
        print('[-] No se puede leer la dirección MAC')

options = get_arguments()
current_mac = get_current_mac(options.interface)
print(f'[+] Dirección MAC actual {current_mac}')

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

if(current_mac == options.new_mac):
    print(f'[+] Dirección MAC cambiada correctamnete a: {current_mac}')
else:
    print('[-] Dirección MAC no fue cambiada')

# Correr comando ifconfig y verificar dirección MAC