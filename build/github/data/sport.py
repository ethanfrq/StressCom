import serial
import serial.tools.list_ports
import socket
import platform
import os
from colorama import init, Fore, Style

init()

def get_machine_info():
    machine_name = platform.node()
    ip_address = socket.gethostbyname(socket.gethostname())
    os_version = platform.platform()
    return machine_name, ip_address, os_version

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def test_serial_port(port):
    try:
        ser = serial.Serial(port, timeout=1)
        ser.close()
        return True
    except (OSError, serial.SerialException):
        return False

def test_packet(ip):
    response = os.system(f"ping -n 1 {ip}")
    if response == 0:
        return True
    else:
        return False

def display_machine_info():
    machine_name, ip_address, os_version = get_machine_info()
    print(f"{Fore.GREEN}Nom : {machine_name}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}IP : {ip_address}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}OS : {os_version}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}\n[ ----------------------------- ]\n{Style.RESET_ALL}")

def display_ports_list():
    ports = list_serial_ports()
    print("Ports disponibles :", ports)

def perform_serial_test():
    ports = list_serial_ports()
    print("Test des ports série...")
    for port in ports:
        if test_serial_port(port):
            print(f"Le port {port} est {Fore.GREEN}disponible et fonctionne{Style.RESET_ALL}.")
        else:
            print(f"Le port {port} n'est {Fore.RED}pas disponible ou ne fonctionne pas{Style.RESET_ALL}.")

if __name__ == "__main__":
    display_machine_info()
    
    while True:
        print("Choisissez une option :")
        print("1. Tester un paquet réseau")
        print("2. Tester les ports série")
        print("3. Lister les ports série")
        print("4. Quitter")
        
        choice = input("Entrez votre choix : ")
        
        if choice == '1':
            ip = input("Entrez l'adresse IP à tester : ")
            if test_packet(ip):
                print(f"Le test de paquet vers {ip} est {Fore.GREEN}réussi{Style.RESET_ALL}.")
            else:
                print(f"Le test de paquet vers {ip} a {Fore.RED}échoué{Style.RESET_ALL}. Veuillez vous assurer que vous avez les privilèges administratifs.")
        elif choice == '2':
            perform_serial_test()
        elif choice == '3':
            display_ports_list()
        elif choice == '4' or choice.lower() == 'exit' or choice.lower() == 'quit':
            print("Fermeture en cours...")
            break
        else:
            print(f"{Fore.RED}Choix invalide. Veuillez réessayer.{Style.RESET_ALL}")

        input("Appuyez sur Entrée pour continuer...")  # Pause avant de réafficher le menu
