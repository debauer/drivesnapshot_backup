Drivesnapshot Backup
====================

<h3>WORK IN PROGRESS</h3>

Ein Python Script für das Kommerzielle Drivesnapshot http://www.drivesnapshot.de/de/ .<br>
Drivesnapshot erstellt 1:1 Images des laufenden Systems und hat uns/mir schon einige male den Arsch gerettet. 

<h2>Benutzung</h2>
Dieser Script macht Backup Cycles mit einem Full Backup und 0-n Differenziellen Backups.
Gedacht für Backups auf einen Fileserver, mit einem Backup Verzeichnis pro User/PC.

<h2>Installation</h2>

Sie benötigen eine Lizenz von Drive SnapShot! http://www.drivesnapshot.de/de/ <br>
Die Scripte sind auf meine Rechner/Server Struktur ausgelegt. 

1. Alle Files in die richtigen Verzeichnisse kopieren.<br>
-> \\server\backup\tools\snapshot.exe<br>
-> \\server\backup\tools\script.py<br>
-> \\server\backup\config.ini<br>
-> C:script\dienst.py

2. Python installieren

3. eventuell Pfad zur Python.exe in dienst.py ändern

4. dienst.py mit vollen Admin Rechen ausstatten. Dafür diese <a href="http://tipps4you.de/tipp-32-win7.html">Anleitung</a> befolgen. 
Statt CCleaner geben Sie die python.exe (z.B. C:\Python33\python.exe) an mit "C:\Script\dienst.py" als Argument.<br>
<b>Alternative:</b><br>
nutzen des start.ps1 Scripts. Das ist ein kleines Batchfile das prüft ob es Adminrechte hat und wenn nicht sich neustartet mit Admin Rechten. Das ist aber nicht sehr elegant und kann auch mal zu Problemen führen.

5. Starten Sie ihre Backups über die erstellte Verknüpfung oder mit start.ps1.

<h2>Mein Setup</h2>

Meine Samba freigaben geben jedem Rechner eine eigene Backup Freigabe. Server seitig sind Scripts/Tools per symlinks in den Backup Verzeichnissen gelinkt. So kann ich das sehr einfach Updaten.
Ich habe die Scripte nicht geschrieben damit sie jeder einfach verwenden kann. Ein wenig Ahnung von Python und Samba/Rechnerstrukturen sollte man schon haben.

Falls du es einsetzen möchtest und es nicht selbst schaffst, dann kann ich dir versuchen zu helfen. 