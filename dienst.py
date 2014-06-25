import os,subprocess,sys,shutil,msvcrt,configparser,smtplib
from subprocess import Popen, PIPE, call
from os import path
from msvcrt import getch
import time
import socket

networkPath = "\\\\fileserv\\Backup\\" 	# ins Netzwerk über WLan Kabel!
drivePath = "Z:" 						# wenns von Platte sein soll
rootPath = networkPath 					# auf networkPath oder drivePath setzen

# File vorhanden wenn nicht beenden
def check_file(path,file):
	if not (os.path.isfile(path + file)):
		return 0
	else:
		return 1

def run_command(cmd):
	process = subprocess.Popen(cmd, shell=True)
	process.wait()


def display_start_error_folder():
	os.system('CLS') # display leeren
	os.system('@TITLE Tagessicherung auf USB-Platte konnte nicht gestartet werden!')
	os.system('@COLOR CF')
	print('')
	print("---------------------------------------------------------------------")
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

if not check_file(rootPath + 'tools\\','script.py'):
	display_start_error_folder()
else:
	run_command('c:\python33\python.exe ' + rootPath + 'tools\\script.py')
