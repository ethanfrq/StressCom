import subprocess

# Chemin du dossier et exécutable
dossier = r"C:\Users\clement.parrot\Desktop\StressCom\sport"
executable = "sport.exe"

# Commande complète
commande = f'cd "{dossier}" && "{executable}"'
print("Lancment reussi")

# Exécution de la commande
subprocess.run(commande, shell=True)
