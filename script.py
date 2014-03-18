import os,subprocess,sys,shutil
from subprocess import Popen, PIPE
from os import path

import configparser

networkPath = "\\\\fileserv\\Backup\\" 	# ins Netzwerk über WLan Kabel!
drivePath = "Z:" 						# wenns von Platte sein soll
rootPath = networkPath 					# auf networkPath oder drivePath setzen
maxCycles = 4;
maxDiff = 1;

# Nicht ändern!
toolPath = rootPath + "tools\\"
backupPath = rootPath + "backups\\"
iniPath = backupPath
# iniPath = backupPath + "status\\"

Config = configparser.ConfigParser()

# ini vorhanden? Wenn nicht default erstellen
def makeConfig(path):
	if not (os.path.isfile(path)):
		cfgfile = open(path,'w')
		Config.add_section('Backup')
		Config.set('Backup','full','0')
		Config.set('Backup','diff','0')
		Config.write(cfgfile)
		cfgfile.close()

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
# checkOrdner(backupPath + "status")	
checkOrdner(backupPath + "cycle1")	

Config = configparser.ConfigParser()

makeConfig(iniPath + "status.ini");

# Config einlesen
Config.read(iniPath + "status.ini")
if(int(Config['Backup']['full']) == 1 and int(Config['Backup']['diff']) == maxDiff):
	i = maxCycles
	# Cycles werden incrementiert und die überzähligen gelöscht.
	while(i):
		if(os.access(backupPath + "cycle" + str(i), os.F_OK)):
			if(i != maxCycles):
				os.rename(backupPath + "cycle" + str(i), backupPath + "cycle" + str(i+1))
			else:
				shutil.rmtree(backupPath + "cycle" + str(i))
		i = i - 1
	# da es nun keinen Cycle1 mehr gibt den Ordner erstellen
	checkOrdner(backupPath + "cycle1")
	





# print(sys.stdout.encoding)

# x = subprocess.Popen(['ping', 'google.de'], stdout=PIPE)
# for line in x.stdout:
	# sys.stdout.write(line.decode(sys.stdout.encoding))
