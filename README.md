# Rocket Beans TV Sendeplan
Ein __Kommandozeilen Sendeplan__ des Web-Senders __Rocket Beans TV__:
* https://www.rocketbeans.tv/ 
* https://www.twitch.tv/rocketbeanstv/
* https://www.rocketbeans.tv/wochenplan/

`rbtv.py` ist ein [Python Skript](https://www.python.org/about/gettingstarted/) welches anhand des  [RBTV Wochenplans](https://www.rocketbeans.tv/wochenplan/) Informationen zum aktuellen Sendeplan in die Kommandozeile ausgibt. Sind alle Abhängigkeiten installiert kann die Datei direkt mit dem _Python Interpreter_ ausgeführt werden.

## Abhängigkeiten
* [Python Interpreter](https://www.python.org/) _(ab Version 3)_
* [requests](http://docs.python-requests.org/) _(Python Modul um die HTML-Seite zu laden)_
* [lxml](http://lxml.de/) _(Python Modul um die HTML-Seite zu parsen)_

## Benutzung
Die Skriptdatei kann mit folgenden Argumenten gestartet werden:
```
usage: rbtv.py [-h] [-c] [-p NROFPASTSHOWS] [-f NROFFUTURESHOWS]

A commandline broadcasting schedule for https://www.twitch.tv/rocketbeanstv

optional arguments:
  -h, --help          show this help message and exit
  -c, --no-color      disable text formatting
  -p NROFPASTSHOWS    set the number of past shows to list (default: 1)
  -f NROFFUTURESHOWS  set the number of future shows to list (default: 6)
```
