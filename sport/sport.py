import serial
import serial.tools.list_ports
import socket
import platform
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Fonctions existantes
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

def list_name_port():
    ports = serial.tools.list_ports.comports()
    if not ports:
        messagebox.showinfo("Info", "Aucun port COM trouvé.")
    else:
        info = ""
        for port in ports:
            info += (f"Port : {port.device}\nNom : {port.name}\nDescription : {port.description}\nEmplacement : {port.location}\n\n")
        messagebox.showinfo("Nom des slots", info)

def display_machine_info():
    machine_name, ip_address, os_version = get_machine_info()
    info = f"Nom : {machine_name}\nIP : {ip_address}\nOS : {os_version}"
    messagebox.showinfo("Informations sur la machine", info)

def display_ports_list():
    ports = list_serial_ports()
    messagebox.showinfo("Ports disponibles", f"Ports disponibles : {', '.join(ports)}")

def perform_serial_test():
    ports = list_serial_ports()
    result = ""
    for port in ports:
        if test_serial_port(port):
            result += f"Le port {port} est disponible et fonctionne.\n"
        else:
            result += f"Le port {port} n'est pas disponible ou ne fonctionne pas.\n"
    messagebox.showinfo("Test des ports série", result)

def detailed_serial_test(port):
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=1)
        ser.write(b'Test')  
        response = ser.read(10)  
        ser.close()
        if response:
            return True
        else:
            return False
    except (OSError, serial.SerialException):
        return False

def perform_detailed_serial_test():
    ports = list_serial_ports()
    result = ""
    for port in ports:
        if detailed_serial_test(port):
            result += f"Le port {port} est disponible et répond.\n"
        else:
            result += f"Le port {port} n'est pas disponible ou ne répond pas.\n"
    messagebox.showinfo("Test détaillé des ports série", result)

def update():
    if check_update_needed():
        try:
            messagebox.showinfo("Mise à jour", "Mise à jour terminée avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour : {e}")
    else:
        messagebox.showinfo("Mise à jour", "Aucune mise à jour nécessaire.")

def check_update_needed():
    return True  # Exemple : toujours retourner True pour simuler des mises à jour nécessaires

def on_test_packet():
    ip = input("Entrez l'adresse IP à tester : ")
    if test_packet(ip):
        messagebox.showinfo("Test de paquet", f"Le test de paquet vers {ip} est réussi.")
    else:
        messagebox.showerror("Test de paquet", f"Le test de paquet vers {ip} a échoué. Veuillez vous assurer que vous avez les privilèges administratifs.")

# Interface graphique
root = tk.Tk()
root.title("Outils de test")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Téléchargement et affichage du logo
response = requests.get("https://www.degreane.fr/app/uploads/sites/145/2022/04/logo_degreane.png")
logo_image = Image.open(BytesIO(response.content))
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(frame, image=logo_photo)
logo_label.grid(row=0, column=0, columnspan=4, pady=10)

# Boutons
ttk.Button(frame, text="Infos Machine", command=display_machine_info).grid(row=1, column=0, padx=10, pady=5)
ttk.Button(frame, text="Ports disponibles", command=display_ports_list).grid(row=1, column=1, padx=10, pady=5)
ttk.Button(frame, text="Nom des slots", command=list_name_port).grid(row=1, column=2, padx=10, pady=5)
ttk.Button(frame, text="Test détaillé", command=perform_detailed_serial_test).grid(row=1, column=3, padx=10, pady=5)
ttk.Button(frame, text="Test Paquet", command=on_test_packet).grid(row=2, column=0, padx=10, pady=5)
ttk.Button(frame, text="Test Série", command=perform_serial_test).grid(row=2, column=1, padx=10, pady=5)
ttk.Button(frame, text="Mise à jour", command=update).grid(row=2, column=2, padx=10, pady=5)
ttk.Button(frame, text="Quitter", command=root.quit).grid(row=2, column=3, padx=10, pady=5)

root.mainloop()
