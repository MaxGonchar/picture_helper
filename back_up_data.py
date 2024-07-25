import shutil
import datetime

def compress_and_backup_data(data_folder, backup_folder):
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Compress the data folder with the timestamp in the filename
    shutil.make_archive(f"{data_folder}_{timestamp}", 'zip', data_folder)
    
    # Move the compressed file to the backup folder
    shutil.move(f"{data_folder}_{timestamp}.zip", backup_folder)

# Specify the paths to the data folder and backup folder
data_folder = "data"
backup_folder = "data_backups"

# Call the function to compress and backup the data folder
compress_and_backup_data(data_folder, backup_folder)