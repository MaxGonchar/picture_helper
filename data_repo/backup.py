import base64
import hashlib
import os
from datetime import datetime
import zipfile

from configs import DATA_FOLDER, DATA_BACKUPS_FOLDER, KEY
from data_repo.indexes import ESIndexes
from cryptography.fernet import Fernet
import shutil

ES_BACKUP_DATA_BATCH_SIZE = 1000
DATETIME_FORMAT = "%Y-%m-%d-%H-%M-%S"


def generate_key(string: str) -> bytes:
    return base64.urlsafe_b64encode(
        hashlib.sha256(string.encode('utf-8')).hexdigest()[:32].encode()
    )


def _create_backup_folder() -> str:
    print("Creating backup folder", end=" ")
    timestamp = datetime.now().strftime(DATETIME_FORMAT)
    folder_name = f"data_{timestamp}"
    backup_folder = os.path.join(DATA_BACKUPS_FOLDER, folder_name)
    os.makedirs(backup_folder)
    print(folder_name)
    return folder_name


def _create_es_backup_folder(backup_folder: str) -> str:
    print("Creating es backup folder")
    es_backup_folder = os.path.join(DATA_BACKUPS_FOLDER, backup_folder, "es")
    os.makedirs(es_backup_folder)
    return es_backup_folder


def _backup_es_data(folder_name: str) -> None:
    print("Backing up ES data")
    es_idx_client = ESIndexes()
    indexes = es_idx_client.get_non_system_indices()

    for index in indexes:
        print(f"Backing up data for index {index}")
        file = os.path.join(folder_name, f"{index}.jsonl")

        with open(file, "w") as f:
            es_idx_client.backup_index_data_to_file(index, f, ES_BACKUP_DATA_BATCH_SIZE)


def _backup_data_folder(folder_name: str) -> None:
    print("Backing up data folder")
    shutil.copytree(
        DATA_FOLDER,
        os.path.join(DATA_BACKUPS_FOLDER, folder_name, DATA_FOLDER)
    )


def _encrypt_folder_files(folder_name: str, key: bytes) -> None:
    print("Encrypting folder files")
    folder_path = os.path.join(DATA_BACKUPS_FOLDER, folder_name)
    fernet = Fernet(key)

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                data = f.read()
            
            encrypted_data = fernet.encrypt(data)
            
            with open(file_path, "wb") as f:
                f.write(encrypted_data)


def _decrypt_folder_files(folder_path: str, key: bytes) -> None:
    print("Decrypting folder files")
    fernet = Fernet(key)

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                data = f.read()
            
            decrypted_data = fernet.decrypt(data)
            
            with open(file_path, "wb") as f:
                f.write(decrypted_data)


def _zip_folder(folder_name: str) -> None:
    print("Zipping folder")
    source_dir = os.path.join(DATA_BACKUPS_FOLDER, folder_name)
    archive_filename = f"{os.path.join(DATA_BACKUPS_FOLDER, folder_name)}.zip"

    with zipfile.ZipFile(archive_filename, "w") as zip_file:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                archive_path = os.path.relpath(file_path, os.path.dirname(source_dir))  # Avoid storing full path in archive
                zip_file.write(file_path, archive_path)


def _delete_folder(folder_path: str) -> None:
    print("Deleting folder")
    shutil.rmtree(folder_path)


def _find_last_backup() -> str:

    def _get_date(path: str) -> datetime:
        _, file = os.path.split(path)
        file_name, _ = os.path.splitext(file)
        datetime_str = file_name.split("_")[-1]
        return datetime.strptime(datetime_str, DATETIME_FORMAT)

    print("Finding last backup")
    backups = [f for f in os.listdir(DATA_BACKUPS_FOLDER) if not f.startswith(".")]

    if not backups:
        raise FileNotFoundError("No backups found")

    backups.sort(key=lambda path: _get_date(path), reverse=True)
    return os.path.join(DATA_BACKUPS_FOLDER, backups[0])


def _unzip_folder(zip_file: str) -> None:
    print("Unzipping folder")
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(DATA_BACKUPS_FOLDER)


def _get_index_files(folder: str) -> list[str]:
    return [file for file in os.listdir(folder) if file.endswith(".jsonl")]


def _restore_es_data(folder: str) -> None:
    print("Restoring ES data")
    for file in _get_index_files(folder):
        with open(os.path.join(folder, file), "r") as f:
            print(f"Restoring data for index {file}")
            index_name, _ = os.path.splitext(file)
            ESIndexes().restore_index_data_from_file(index_name, f)


def _restore_data_folder(folder: str) -> None:
    print("Restoring data folder")
    src_folder = os.path.join(folder, DATA_FOLDER)
    for item in os.listdir(src_folder):
        s = os.path.join(src_folder, item)
        d = os.path.join(DATA_FOLDER, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)


def do_backup():
    backup_folder = _create_backup_folder()
    es_backup_folder = _create_es_backup_folder(backup_folder)
    _backup_es_data(es_backup_folder)
    _backup_data_folder(backup_folder)
    _encrypt_folder_files(backup_folder, generate_key(KEY))
    _zip_folder(backup_folder)
    _delete_folder(os.path.join(DATA_BACKUPS_FOLDER, backup_folder))


def do_restore():
    last_backup_zip = _find_last_backup()
    last_backup_folder = os.path.splitext(last_backup_zip)[0]

    if not input(f"Are you sure you want to restore data from {last_backup_zip}? (y/n): ").lower().startswith("y"):
        return

    _unzip_folder(last_backup_zip)
    _decrypt_folder_files(last_backup_folder, generate_key(KEY))
    _restore_es_data(os.path.join(last_backup_folder, "es"))
    _restore_data_folder(last_backup_folder)
    _delete_folder(last_backup_folder)
