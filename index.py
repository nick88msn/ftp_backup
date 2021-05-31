import sys
import ftplib
import os
from ftplib import FTP
from pathlib import Path
import secrets

ftp=FTP(secrets.HOST)
ftp.login(secrets.USER,secrets.PASSWORD)

def downloadFiles(path,destination):
#path & destination are str of the form "/dir/folder/something/"
#path should be the abs path to the root FOLDER of the file tree to download
    try:
        ftp.cwd(path)
        #clone path to destination
        Path(destination[0:len(destination)-1]+path).mkdir(parents=True, exist_ok=True)
        os.chdir(destination[0:len(destination)-1]+path)
        print(destination[0:len(destination)-1]+path+" built")
    except OSError:
        #folder already exists at destination
        pass
    except ftplib.error_perm:
        #invalid entry (ensure input form: "/dir/folder/something/")
        print("error: could not change to "+path)
        sys.exit("ending session")

    #list children:
    filelist=ftp.nlst()

    for file in filelist:
        try:
            #this will check if file is folder:
            ftp.cwd(path+file+"/")
            #if so, explore it:
            print(f"{path}{file}/")
            downloadFiles(path+file+"/",destination)
        except ftplib.error_perm:
            #not a folder with accessible content
            #download & return
            os.chdir(destination[0:len(destination)-1]+path)
            #possibly need a permission exception catch:
            print(os.path.join(destination[0:len(destination)-1],path,file))
            with open(os.path.join(destination[0:len(destination)-1],path,file),"wb") as f:
                ftp.retrbinary("RETR "+file, f.write)
                print(file + " downloaded")
    return

source="/"
dest="/Volumes/wd_blue/backup/server/register/"
downloadFiles(source,dest)