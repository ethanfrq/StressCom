import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import time
import logging
import requests
from PIL import Image, ImageTk
from io import BytesIO
from colorama import init, Fore, Style
init()

class ColorFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: Fore.BLUE + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + "%(asctime)s - %(levellevelname)s - %(message)s" + Style.RESET_ALL,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self._fmt)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(ColorFormatter())
logger.addHandler(ch)

base_dir = os.path.expanduser("~/Desktop/StressCom")
files_structure = {
    "build": {
        "pip.txt": "pip install -r requirements.txt",
        "r.bat": "@echo off\npython -m pip install --upgrade pip",
        "requirements.txt": "pip install colorama pyserial pyinstaller requests Pillow"
    },
    "sport": {
        "genexe.bat": r"""@echo off
setlocal EnableDelayedExpansion

set "script_path="
set /p script_path="Entrez le chemin complet du script Python (.py) : "

set "exe_name="
set /p exe_name="Entrez le nom du fichier executable de sortie (sans extension) : "

echo Verification de l'installation de PyInstaller...
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller n'est pas installe. Installation en cours...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Echec de l'installation de PyInstaller. Verifiez votre installation de Python et pip.
        exit /b 1
    ) else (
        echo PyInstaller a ete installe avec succes.
    )
) else (
    echo PyInstaller est deja installe.
)

echo Creation de l'executable...
pyinstaller --onefile --name %exe_name% "%script_path%" >nul 2>&1

set "bar=."
for /L %%i in (1,1,50) do (
    set /p "=." <nul
    ping -n 2 127.0.0.1 >nul 2>&1
)
echo.

if exist "dist\%exe_name%.exe" (
    echo L'executable a ete cree avec succes : dist\%exe_name%.exe
) else (
    echo Echec de la creation de l'executable. Verifiez les logs pour plus de details.
)

echo Affichage des logs...
type "dist\%exe_name%.exe"
echo.

pause
""",
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

        input("Appuyez sur Entrée pour continuer...")"""
    },
    "spoints": {
        "get-pip.py": "https://bootstrap.pypa.io/get-pip.py"
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

def install():
    logger.info("Démarrage de l'installation")
    progress_bar["value"] = 0
    root.update()
    create_files()
    increment = 100 / (5 * 10)  
    for i in range(50):
        progress_bar["value"] += increment
        root.update()
        time.sleep(0.1)
    progress_bar["value"] = 100
    messagebox.showinfo("Installation", "Installation terminée avec succès !")
    logger.info("Installation terminée avec succès")

def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def update():
    logger.info("Démarrage de la mise à jour")
    progress_bar["value"] = 0
    root.update()

    if check_update_needed():
        if check_internet_connection():
            if os.path.exists("StressComMaj"):
                shutil.rmtree("StressComMaj")
            
            download_url = "https://github.com/ethanfrq/StressComMaj/archive/main.zip"
            response = requests.get(download_url)
            
            if response.status_code == 200:
                with open("StressComMaj.zip", "wb") as f:
                    f.write(response.content)
               
                messagebox.showinfo("Mise à jour", "Mise à jour terminée avec succès !")
                logger.info("Mise à jour terminée avec succès")
            else:
                messagebox.showerror("Erreur de mise à jour", "Échec du téléchargement des fichiers de mise à jour.")
                logger.error("Échec du téléchargement des fichiers de mise à jour.")
        else:
            messagebox.showerror("Erreur de mise à jour", "Aucune connexion Internet. Veuillez vous connecter pour mettre à jour.")
            logger.error("Aucune connexion Internet. Impossible de mettre à jour.")
    else:
        messagebox.showinfo("Mise à jour", "Aucune mise à jour nécessaire.")
        logger.info("Aucune mise à jour nécessaire.")

    progress_bar["value"] = 100

def check_update_needed():
    try:
        version_url = "https://raw.githubusercontent.com/ethanfrq/StressComMaj/main/version.txt"
        
        current_version = get_current_version() 
        
        response = requests.get(version_url)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version > current_version:
                return True 
            
        return False
    
    except Exception as e:
        logging.ERROR(f"Erreur lors de la vérification des mises à jour : {e}")
        return False

def get_current_version():
    return "1.0.0"  
if check_update_needed():
    logger.warning("Mise à jour nécessaire.")
else:
    logger.info("Aucune mise à jour nécessaire.")

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

def developer():
    logger.info("Ouverture de la fenêtre modale Développeur")
    messagebox.showinfo("Info developer", "Cette application a été développée par Ethan Franqueville developer pour VOOT - Group, etudiant en bts 1 année au Lycee La Cordeille")

def enterprise():
    logger.info("Ouverture du site de Degreane")
    webbrowser.open("https://www.degreane.fr/")

def run():
    logger.info("Démarrage de l'exécution")
    #os.system('python sport/run.py')
    os.system('python sport/sport.py')
    logger.info("Exécution terminée.")
     
root = tk.Tk()
root.title("Installateur StressCom | Degreane Citeos")

response = requests.get("https://www.degreane.fr/app/uploads/sites/145/2022/04/logo_degreane.png")
logo_image = Image.open(BytesIO(response.content))
logo_photo = ImageTk.PhotoImage(logo_image)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

logo_label = tk.Label(frame, image=logo_photo)
logo_label.grid(row=0, column=0, columnspan=6, pady=10)

ttk.Button(frame, text="Installer", command=install).grid(row=1, column=0, padx=10, pady=5)
ttk.Button(frame, text="MAJ", command=update).grid(row=1, column=1, padx=10, pady=5)
ttk.Button(frame, text="Run", command=run).grid(row=1, column=2, padx=10, pady=5)
ttk.Button(frame, text="Désinstaller", command=uninstall).grid(row=1, column=3, padx=10, pady=5)

ttk.Button(frame, text="Développeur", command=developer).grid(row=2, column=0, padx=10, pady=5)
ttk.Button(frame, text="Entreprise", command=enterprise).grid(row=2, column=1, padx=10, pady=5)
ttk.Button(frame, text="GitHub", command=lambda: webbrowser.open("https://github.com/ethanfrq")).grid(row=2, column=2, padx=10, pady=5)
ttk.Button(frame, text="À propos", command=about).grid(row=2, column=3, padx=10, pady=5)

ttk.Button(frame, text="Quitter", command=root.quit).grid(row=3, column=1, padx=10, pady=5)


progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=6, padx=10, pady=10)

root.mainloop()