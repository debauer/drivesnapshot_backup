
import urllib.request

server = "http://fileserv:1337"

urllib.request.urlopen(server + "/Backup/create?hostname=pc2&drive=d")
#def safe_status():
	# Status soll in der Datenbank gespeichert werden.
	#urllib2.urlopen("fileserv:1337/Backup/create?hostname=pc2&drive=d")
	