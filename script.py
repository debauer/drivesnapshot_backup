import os,subprocess,sys
from subprocess import Popen, PIPE
from os import path

import configparser

networkPath = "\\\\fileserv\\Backup\\" # ins Netzwerk über WLan Kabel!
drivePath = "Z:" # wenns von Platte sein soll
rootPath = networkPath # auf networkPath oder drivePath setzen
maxCycles = 3;
maxDiff = 1;

# Nicht ändern!
toolPath = rootPath + "tools\\"
backupPath = rootPath + "backups\\"
iniPath = backupPath + "status\\"

Config = configparser.ConfigParser()

# File vorhanden wenn nicht beenden
def checkFile(path,file):
	if not (os.path.isfile(path + file)):
		print("File: " + file + " ist nicht Vorhanden")
		input("ENTER drücken zum Beenden")
		sys.exit();
	
# Ordner vorhanden wenn nicht erstellen
def checkOrdner(path):
	if not (os.access(path, os.F_OK)):
		os.mkdir(path)
	
	
# Checken ob alle benötigten Ordner/Files vorhanden sind
checkFile(toolPath,"snapshot.exe")
checkOrdner(rootPath + "tools")
checkOrdner(rootPath + "backups")
checkOrdner(backupPath + "status")	
checkOrdner(backupPath + "cycle1")	

# ini vorhanden? Wenn nicht default erstellen
if not (os.path.isfile(iniPath + "status1.ini")):
	cfgfile = open(iniPath + "status1.ini",'w')
	Config.add_section('Backup')
	Config.set('Backup','full','0')
	Config.set('Backup','diff','0')
	Config.write(cfgfile)
	cfgfile.close()


Config = Config.read(iniPath + "status1.ini")
if(Config.get("Backup","full") == 1 and Config.get("Backup","diff") == maxDiff):
	# neuer Cycle
	# Cycles umbenennen
	i = maxCycles
	while(i):
		if(os.path.isfile(iniPath + "status" + i + ".ini")):
			if(i != maxCycles):
				os.rename(iniPath + "status" + i + ".ini", iniPath + "status" + (i+1) + ".ini")
			else:
				os.remove(iniPath + "status" + i + ".ini")			
		if(os.access(backupPath + "cycle" + i, os.F_OK)):
			if(i != maxCycles):
				os.rename(backupPath + "cycle" + i, backupPath + "cycle" + (i+1))
			else:
				os.rmdir(backupPath + "cycle" + i)
		i = i - 1



# print(sys.stdout.encoding)

x = subprocess.Popen(['ping', 'google.de'], stdout=PIPE)
for line in x.stdout:
	sys.stdout.write(line.decode(sys.stdout.encoding))
