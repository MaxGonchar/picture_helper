#### start db
`./db.sh up`

#### stop db
`./db.sh down`

#### backups
##### do backups
make sure that db is run
execute `python backup.py -d` - script creates a zip file in `data_backups` folder
##### restore backups
make sure that zip file with backups is present in the `data_backups` folder
make sure that db is run
clear data indeces in ES  (TODO: automate process)
clear the `data` folder (delete all files and folders inside) (TODO: automate process)
execute `python backup.py -r`

#### rate images
`python image_rater.py`

#### open gui
`python gui.py`

#### generate ids if pictures to analyze
`python ids_generator.py -s <int> -e <int>`
for example `python ids_generator.py -s 1000000 -e 1999999`
