# Installation
1. Xibo CMS auf einem Server mit Docker installieren: https://xibo.org.uk/docs/setup/xibo-for-docker
2. Mit ```docker container ls``` die installierten Container auflisten und die ContainerID des XiboCMS Containers kopieren.
3. Mit ```docker exec -it <ID> /bin/bash``` eine Shell im Container öffnen (\<ID> durch die ContainerID ersetzen)
4. Python im Container installieren: ```apk add --no-cache python3```
5. Den Ordner /opt erstellen: ```mkdir /opt```
6. Den Container mit ```exit``` verlassen
7. In der Datei CipPools/untis2.py in Zeile 93 und 94 den Benutzernamen und das Passwort eines gültigen WebUntis nutzers der OTH Regensburg eintragen
8. Den Ordner CipPools nach /opt in den Container kopieren: ```docker cp CipPools/ <ID>:/opt```
9. Den Inhalt des Ordners userscripts dieses Repos nach /opt/xibo/cms/web/userscripts auf dem Server kopieren.
10. Die beiden ZIP Dateien in Layouts im Xibo CMS importieren.
11. ggf. Die IP Adressen in den importierten Layouts und Datensätzen anpassen.
