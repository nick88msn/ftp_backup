# FTP Backup

A little script to download recursively all folders and files from an ftp server.
Remote Entry point is the first argument of the script. 
Destination local folder is the second argument of the script.

## Installation

```Python
pip3 install -r requirements.txt
```

Create a secrets.py file and add the following information:
```Python3
HOST = 'ftp.yourwebserver.com'
USER='your_username'
PASSWORD='some_compliCATeD_P4SSwD'
```

```Python
python3 index.py source destination
```