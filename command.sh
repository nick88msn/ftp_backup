#!/bin/sh

#inside pipenv shell
#BIOFEEDSTOCK (ARS01_00985)
pipenv run python3 /Users/nicolamastrandrea/repo/ftp/index.py "public/reddoc/upload/files/richieste/" "/Users/nicolamastrandrea/Documents/reddoc"

rsync -avP --progress --delete /Users/nicolamastrandrea/Documents/reddoc/ /Users/nicolamastrandrea/Documents/piattaforma/

python3 /Users/nicolamastrandrea/repo/traduttoreReddoc/main.py /Users/nicolamastrandrea/Documents/piattaforma/public/reddoc/upload/files/richieste

rsync -avP --progress --delete "/Users/nicolamastrandrea/Documents/piattaforma/public/reddoc/upload/files/richieste/BIOFEEDSTOCK (ARS01_00985)/" "/Users/nicolamastrandrea/OneDrive/Biofeedstock (nicola)/100._Piattaforma_Reddoc"

DIRECTORY='/Users/nicolamastrandrea/OneDrive/Biofeedstock (nicola)/100._Piattaforma_Reddoc/'
cd $DIRECTORY
for i in */; do zip -0 -r "${i%/}.zip" "$i" & done; wait
find . -type d -exec rm -rf {} +
