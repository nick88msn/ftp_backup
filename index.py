import sys
import ftputil
import argparse
import os
from pathlib import Path
import secrets


# Parse user arguments from cli
def parse_args():
    parser = argparse.ArgumentParser(description='Backup a server or a folder through ftp protocol')
    parser.add_argument("source", type=str, help="Add absolute path without beginning or ending /", default=''))
    parser.add_argument("destination", type=str, help="Destination folder of the final mbox file. If ", default=os.path.join(os.getcwd(),'backup'))
    args = parser.parse_args()
    return args


def downloadFiles(path,destination):
    # Connect to host
    with ftputil.FTPHost(secrets.HOST,secrets.USER,secrets.PASSWORD) as ftp_host:
        try:
            # Input source formatted as "path/to/directory"
            ftp_host.chdir(path)
            print(f"Changed ftp directory to: {path}")
            current_local_folder = os.path.join(destination,path)
            print(f"Updated current local folder to: {current_local_folder}")
            Path(current_local_folder).mkdir(parents=True, exist_ok=True)
            print(f"{os.path.join(destination,path)} created.")
            list = ftp_host.listdir(ftp_host.curdir)
            print(f"List of ftp folders and files:\n{list}")
            for fname in list:
                if ftp_host.path.isdir(fname):
                    #launch recursive function with new source
                    downloadFiles(os.path.join(path,fname),destination)
                else:
                    #download files in current destination folder
                    try:
                        ftp_host.synchronize_times()
                        ftp_host.download_if_newer(os.path.join(fname),os.path.join(current_local_folder,fname))
                    except ftputil.error.TimeShiftError as e:
                        print(f"Could not sync timestamps with server. Forcing download")
                        ftp_host.download(os.path.join(fname),os.path.join(current_local_folder,fname))

                    print(f"Downloaded {os.path.join(path,fname)} in path {os.path.join(current_local_folder,fname)}")
        except OSError as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    args = parse_args()
    source=args.source
    dest=args.destination
    downloadFiles(source,dest)