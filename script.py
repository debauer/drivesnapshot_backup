import os,subprocess,sys,shutil,msvcrt,configparser,smtplib
from subprocess import Popen, PIPE, call
from os import path
from msvcrt import getch
import time
import socket
import urllib.request

# V0.2


# ======================================================================================================================
# ======================================================================================================================
#	Base Conf
# ======================================================================================================================

networkPath = "\\\\fileserv\\Backup\\" 	# ins Netzwerk über WLan Kabel!
drivePath = "Z:" 						# wenns von Platte sein soll
rootPath = networkPath 					# auf networkPath oder drivePath setzen

apiURL = "http://fileserv:9000/Backup"

# ======================================================================================================================
# ======================================================================================================================
#	Funktionen
# ======================================================================================================================



# ini vorhanden? Wenn nicht default erstellen
def make_status(path):
	statusfile = open(path,'w')
	status.add_section('AKT')
	status.set('AKT','full','0')
	status.set('AKT','diff','0')
	status.set('AKT','run','false')
	status.write(statusfile)
	statusfile.close()



# File vorhanden wenn nicht beenden
def check_file(path,file):
	if not (os.path.isfile(path + file)):
		return 0
	else:
		return 1

# Programm beenden
def beenden():
	input("ENTER drücken zum Beenden")
	sys.exit()

# Ordner vorhanden wenn nicht erstellen
def check_ordner(path):
	if not (os.access(path, os.F_OK)):
		print("0: " + path)
		return 0
	else:
		print("1: " + path)
		return 1

# Ordner erstellen
# Python scheint asyncron zu arbeiten was Betriebsystem/Filesystem zugriff angeht.
# os.access(path, os.F_OK) meldet vereinzelt gelöschte Ordner als vorhanden.
# Könnte auch nur mitm Netzwerk Share zutun haben.
def make_ordner(path):
	try:
		os.mkdir(path)
	except OSError:
		pass

#system herunterfahren
def herunterfahren():
	os.system('shutdown -s -f')


# Backup + Verify
def make_backup(drive,diff = 0):
	print('')
	print("=====================================================================")
	print('---- Partion-Sicherung: ' + drive + ': ' + time.strftime("%d/%m/%Y") + ' ----')
	print("=====================================================================")
	print('')
	backup_folder = backupPath + 'cycle1\\' + drive + "_drive"
	make_ordner(backup_folder)
	#print(toolPath + 'snapshot.exe ' + drive + ': ' + backup_folder + '\\' + drive + '_full.sna' + ' -W ')
	if diff:
		process = subprocess.Popen(toolPath + 'snapshot.exe ' + drive + ': ' + backup_folder + '\\' + drive + '_diff' + str(diff) + '.sna' + ' -h' + backup_folder + '\\' + drive + '_full.hsh -W ', shell=True)
	else:
		process = subprocess.Popen(toolPath + 'snapshot.exe ' + drive + ': ' + backup_folder + '\\' + drive + '_full.sna' + ' -W ', shell=True)
	process.wait()
	errorcode = process.returncode
	process.kill()
	print('')
	print('---- Backup wird Verifiziert ----')
	print('')
	if diff:
		process = subprocess.Popen(toolPath + 'snapshot.exe ' + backup_folder + '\\' + drive + '_diff' + str(diff) + '.sna' + ' -T -W ', shell=True)
	else:
		process = subprocess.Popen(toolPath + 'snapshot.exe ' + backup_folder + '\\' + drive + '_full.sna' + ' -T -W ', shell=True)
	process.wait()
	errorcode = process.returncode
	process.kill()
	print('')
	print('---- Partition-Sicherung beendet ----')
	print('')
# FUNKTIONSENDE


def new_circle():
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
	if not check_ordner(backupPath + "cycle1"):
		make_ordner(backupPath + "cycle1")

def send_mail():

	if(config['EMAIL']['aktiv'] == "true"):
		smtpserver = config['EMAIL']['server'] # SMTP server
		port = config['EMAIL']['port']
		username = config['EMAIL']['user']  # for SMTP AUTH, set SMTP username here
		password = config['EMAIL']['pw']  # for SMTP AUTH, set SMTP password here
		sender = config['EMAIL']['sender']
		to = config['EMAIL']['to']
		protocol = config['EMAIL']['protocol']

		subject = 'Backup wurde beendet'
		text = "GOIL"
		headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, to, subject)
		message = headers + text
		try:
			#Send the email
			session = smtplib.SMTP()
			session.connect(smtpserver, int(port))
			#session.set_debuglevel(1)
			if str(protocol).lower() == "ssl" :
				session.starttls()
			session.login(username, password)
			session.sendmail(sender, to, message)
			session.quit()#
		except Exception as exc:
			if verbose:
				print("eMail senden fehlgeschlagen")


def safe_status():
	# Status soll in der Datenbank gespeichert werden.
	dbname 		= "it"
	dbserver 	= "fileserv"
	dbuser		= "it"
	dbpw 		= "opti"

def display_startmenue():
	if(int(status['AKT']['full']) == 1):
		state = "Differenziell"
	else:
		state = "Vollbackup"
	os.system('CLS') # display leeren
	os.system('@TITLE Tagessicherung: Startmenue')
	os.system('@COLOR 9F')
	print("================================================== Version " + version + "  =====")
	print("  Autor: David Bauer, Schlager GmbH			")
	print("---------------------------------------------------------------------")
	print("																		")
	print("  TAGESSICHERUNG                                 *** "+ state + " ***")
	print("  -------------- 													")
	print("  [S] == SICHERN														")
	print("  [B] == Beides, SICHERN und anschliessend HERUNTERFAHREN			")
	print("  [F] == Full Backup erzwingen										")
	print("  [X] == Exit (Abbrechen)											")
	print("																		")
	print("  HINWEIS: 															")
	print("  Notebooks unbedingt am Stromnetz betreiben!						")
	print("=====================================================================")
	falscheTaste = 1
	while(falscheTaste):
		taste = getch().decode(sys.stdout.encoding)
		falscheTaste = 0
		if taste == 's' or taste == 'S':
			modus = 'NORMAL'
		elif taste == 'b' or taste == 'B':
			modus = 'NORMAL'
			shutdown = 1
		elif taste == 'f' or taste == 'F':
			modus = 'FORCE'
		elif(taste == 'x' or taste == 'X'):
			sys.exit(); # beenden
		else:
			falscheTaste = 1
	os.system('CLS') # display leeren
# FUNKTIONSENDE

def display_backup_error():
	os.system('@TITLE Tagessicherung FEHLERHAFT!')
	os.system('@COLOR CF')
	print('')
	print("-------------------------------------------------- Version " + version + " -----")
	print(' Die Tagessicherung war abgeschlossen am ' + time.strftime("%d/%m/%Y") + ' um ' + time.strftime("%H:%M:%S") + ' Uhr')
	print(' Es sind Fehler aufgetreten!')
	print('')
	print(' Hinweis: Informieren Sie unbedingt den Administrator!')
	print('---------------------------------------------------------------------')
	print('')
	beenden()

def display_backup_ok():
	os.system('@TITLE Tagessicherung abgeschlossen!')
	os.system('@COLOR 2F')
	print('')
	print("-------------------------------------------------- Version " + version + " -----")
	print(' Die Tagessicherung war abgeschlossen am ' + time.strftime("%d/%m/%Y") + ' um ' + time.strftime("%H:%M:%S") + ' Uhr')
	print('')
	print(' Sie koennen das Protokoll in diesem Fenster scrollen.')
	print('---------------------------------------------------------------------')
	print('')
	if(shutdown):
		herunterfahren()
	beenden()


def display_start_error_folder():
	os.system('CLS') # display leeren
	os.system('@TITLE Tagessicherung auf USB-Platte konnte nicht gestartet werden!')
	os.system('@COLOR CF')
	print('')
	print("-------------------------------------------------- Version " + version + " -----")
	print('')
	print(' F E H L E R:')
	print(' ------------')
	print('')
	print(' Der Zielordner fuer die Sicherung wurde nicht gefunden !!!')
	print(' Erwarteter Zielordner ist: ' + networkPath)
	print('')
	print('---------------------------------------------------------------------')
	print('')
	beenden()

def display_start_error_file(file):
	os.system('CLS') # display leeren
	os.system('@TITLE Tagessicherung auf USB-Platte konnte nicht gestartet werden!')
	os.system('@COLOR CF')
	print('')
	print("-------------------------------------------------- Version " + version + " -----")
	print('')
	print(' F E H L E R:')
	print(' ------------')
	print('')
	print(' Ein File fuer die Sicherung wurde nicht gefunden !!!')
	print(" File: " + file + " ist nicht Vorhanden")
	print('')
	print('---------------------------------------------------------------------')
	print('')
	beenden()

def display_start_error_second():
	os.system('CLS') # display leeren
	os.system('@TITLE Sicherung kann nicht mehrfach gestartet werden!')
	os.system('@COLOR E4')
	print('')
	print("-------------------------------------------------- Version " + version + " -----")
	print('')
	print(' W A R N U N G !!')
	print(' ----------------')
	print('')
	print(' Eine Sicherung kann derzeit nicht gestartet werden!')
	print(' Warten Sie, bis die aktuell laufende Sicherung abgeschlossen ist!')
	print('')
	print(' HINWEIS: Diese Meldung wird auch angezeigt, wenn eine fruehere')
	print(' Sicherung nicht korrekt beendet wurde.')
	print(' Informieren Sie in diesem Fall den Administrator!')
	print('')
	print('---------------------------------------------------------------------')
	print('')
	beenden()


# ======================================================================================================================
# ======================================================================================================================
#                                                   Main CODE!
# ======================================================================================================================

version = ' 0.1'
modus = 'NORMAL'
shutdown = 0
verbose = 1
errorcode = 0
hostname = socket.gethostname()

# Nicht ändern!
toolPath = rootPath + "tools\\"
backupPath = rootPath + "backups\\"
iniPath = backupPath
# iniPath = backupPath + "status\\"

status = configparser.ConfigParser()
config = configparser.ConfigParser()


# Checken ob alle benötigten Ordner/Files vorhanden sind

# rootpath erreichbar?!
if not (os.access(rootPath, os.F_OK)):
	display_start_error_folder()

# Alle files vorhanden?
if not check_file(toolPath,"snapshot.exe"):
	display_start_error_file(toolPath + "snapshot.exe")

if not check_file(toolPath,"config.ini"):
	display_start_error_file(toolPath + "config.ini")

# Ordnerstruktur checken
if not check_ordner(rootPath + "tools"):
	make_ordner(rootPath + "tools")

if not check_ordner(rootPath + "backups"):
	make_ordner(rootPath + "backups")

if not check_ordner(backupPath + "cycle1"):
	make_ordner(backupPath + "cycle1")

if not check_file(iniPath, "status.ini"):
	make_status(iniPath + "status.ini")

# Status einlesen
status.read(iniPath + "status.ini")

# Config einlesen
config.read(toolPath + "config.ini")

maxCycles = int(config['BACKUP']['cycles'])
maxDiff = int(config['BACKUP']['diff'])
drives = config.items( "DRIVES" )

full = int(status['AKT']['full'])
diffs = int(status['AKT']['diff'])
run = status['AKT']['run']

if run == 'true': #woops, letztes backup hat gefailed
	urllib.request.urlopen(apiURL + "/create?hostname=" + hostname + "&status=ERROR&error=last backup has failed")
	display_start_error_second()

# lets gooo
display_startmenue()
urllib.request.urlopen(apiURL + "/create?hostname=" + hostname + "&status=START&modus=" + modus)

status['AKT']['run'] = 'true'
with open(iniPath + "status.ini", 'w') as statusfile:
    status.write(statusfile)

# Wenn Circle voll ist einen neuen starten
if full == 1 and diffs == maxDiff :
	new_circle()
	status['AKT']['full'] = '0'
	status['AKT']['diff'] = '0'
	full = 0
	diffs = 0
	with open(iniPath + "status.ini", 'w') as statusfile:
		status.write(statusfile)

# jetzt wird gebackupt!!!
for key, drive in drives:
	# drive = Laufwerksnummer
	if full:
		urllib.request.urlopen(apiURL + "/create?hostname=" + hostname + "&status=DIFF&modus=" + modus + "&drive=" + drive + "&circle=" + str(diffs))
		make_backup(drive,diffs+1)
	else:
		urllib.request.urlopen(apiURL + "/create?hostname=" + hostname + "&status=FULL&modus=" + modus + "&drive=" + drive)
		make_backup(drive)

if not full:
	status['AKT']['full'] = '1'
	status['AKT']['diff'] = '0'
else:
	status['AKT']['diff'] = str(diffs+1)
status['AKT']['run'] = 'false'
with open(iniPath + "status.ini", 'w') as statusfile:
	status.write(statusfile)
	
	
# Backup zuende
#send_mail()
urllib.request.urlopen(apiURL + "/create?hostname=" + hostname + "&status=OK&modus=" + modus)
display_backup_ok()

# Vielen dank an Johannes Bozenhardt!