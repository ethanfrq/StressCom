import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import time
import logging
from colorama import init, Fore, Style

# Initialisation de colorama
init()

# Configurer les logs avec des couleurs
class ColorFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: Fore.BLUE + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self._fmt)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Configurer le logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(ColorFormatter())
logger.addHandler(ch)

# Chemins et fichiers
base_dir = "StressCom"
files_structure = {
    "build": {
        "pip.py": "pip install -r requirements.txt",
        "r.bat": "@echo off\npython -m pip install --upgrade pip"
    },
    "sport": {
        "sport.py": """import serial
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
    print(f"{Fore.YELLOW}\\n[ ----------------------------- ]\\n{Style.RESET_ALL}")

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

        input("Appuyez sur Entrée pour continuer...")""",
        "logs.py": "import logging\n\n# Your logging setup here"
    },
    "spoints": {
        "get-pip.py": "# Your get-pip.py script here"
    }
}

def create_files():
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        logger.info(f"Création du répertoire de base : {base_dir}")
    
    for folder, files in files_structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        logger.info(f"Création du dossier : {folder_path}")
        for file, content in files.items():
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'w') as f:
                f.write(content)
            logger.info(f"Création du fichier : {file_path}")

def verify_files():
    missing_files = []
    for folder, files in files_structure.items():
        folder_path = os.path.join(base_dir, folder)
        if not os.path.exists(folder_path):
            missing_files.append(folder_path)
            continue
        for file in files:
            file_path = os.path.join(folder_path, file)
            if not os.path.exists(file_path):
                missing_files.append(file_path)
    return missing_files

def update_files():
    missing_files = verify_files()
    if not missing_files:
        messagebox.showinfo("Mise à jour", "Tous les fichiers sont présents et complets.")
        logger.info("Tous les fichiers sont présents et complets.")
    else:
        for path in missing_files:
            if os.path.isdir(path):
                os.makedirs(path, exist_ok=True)
                logger.info(f"Création du dossier manquant : {path}")
            else:
                folder, file = os.path.split(path)
                content = files_structure.get(os.path.basename(folder), {}).get(file, "")
                with open(path, 'w') as f:
                    f.write(content)
                logger.info(f"Création du fichier manquant : {path}")
        messagebox.showinfo("Mise à jour", f"Les fichiers suivants ont été créés :\n{missing_files}")

def delete_files():
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
        logger.info(f"Suppression du répertoire : {base_dir}")

# Actions des boutons
def install():
    logger.info("Démarrage de l'installation")
    progress_bar["value"] = 0
    root.update()
    create_files()
    
    increment = 100 / (5 * 10)  # 5 seconds divided into 10 increments per second

    for i in range(50):
        progress_bar["value"] += increment
        root.update()
        time.sleep(0.1)

    progress_bar["value"] = 100
    messagebox.showinfo("Installation", "Installation terminée avec succès !")
    logger.info("Installation terminée avec succès")

def update():
    logger.info("Démarrage de la mise à jour")
    progress_bar["value"] = 0
    root.update()
    update_files()

    increment = 100 / (5 * 10)  # 5 seconds divided into 10 increments per second

    for i in range(50):
        progress_bar["value"] += increment
        root.update()
        time.sleep(0.1)

    progress_bar["value"] = 100
    messagebox.showinfo("Mise à jour", "Mise à jour terminée avec succès !")
    logger.info("Mise à jour terminée avec succès")

def uninstall():
    logger.info("Démarrage de la désinstallation")
    delete_files()
    messagebox.showinfo("Désinstallation", "Désinstallation terminée avec succès !")
    logger.info("Désinstallation terminée avec succès")

def open_github():
    logger.info("Ouverture de GitHub")
    webbrowser.open("https://github.com/ethanfrq")

def about():
    logger.info("Affichage de la boîte de dialogue À propos")
    messagebox.showinfo("À propos", "Cette application a été développée par Ethan Franqueville pour l'entreprise Citeos Degreane. Tous droits réservés.")

# Interface graphique
root = tk.Tk()
root.title("Installateur StressCom")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Button(frame, text="Installer", command=install).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(frame, text="MAJ", command=update).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(frame, text="Désinstaller", command=uninstall).grid(row=0, column=2, padx=10, pady=5)
ttk.Button(frame, text="GitHub", command=open_github).grid(row=0, column=3, padx=10, pady=5)
ttk.Button(frame, text="À propos", command=about).grid(row=0, column=4, padx=10, pady=5)

progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

root.mainloop()
