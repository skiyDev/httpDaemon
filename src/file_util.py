import os
import shutil
import uuid
import hashlib


class FileHelper:
    """
    save and calc hash for file
    """
    def __init__(self):
        self.__basepath = '/store/'

    def __check_dir(self, dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    async def save_file(self, field):
        self.__check_dir(self.__basepath)

        filename = str(field.filename)
        temp_folder = os.path.join(self.__basepath, uuid.uuid4().hex)
        self.__check_dir(temp_folder)

        temp_filename = os.path.join(temp_folder, filename)
        hash_md5 = hashlib.md5()
        with open(temp_filename, 'wb') as file:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break

                file.write(chunk)
                hash_md5.update(chunk)

        hashsum = hash_md5.hexdigest()
        self.__move_file(hashsum, temp_filename)
        return hashsum

    def __move_file(self, hash, temp_fname):
        dist_path = os.path.join(self.__basepath, hash[:2])
        dist_file = os.path.join(dist_path, hash)
        temp_path = os.path.dirname(temp_fname)
        hash_fname = os.path.join(temp_path, hash)

        if not os.path.isdir(dist_path):
            os.rename(temp_fname, hash_fname)
            os.rename(temp_path, dist_path)
        elif not os.path.isfile(dist_file):
            os.rename(temp_fname, hash_fname)
            shutil.move(hash_fname, dist_file)
            shutil.rmtree(temp_path)
        else:
            os.remove(temp_fname)
            shutil.rmtree(temp_path)

    def get_filepath_by_hash(self, hash: str):
        dist_path = os.path.join(self.__basepath, hash[:2])
        dist_file = os.path.join(dist_path, hash)
        if os.path.isfile(dist_file):
            return dist_file

    def remove_file_by_hash(self, hash: str):
        dist_path = os.path.join(self.__basepath, hash[:2])
        dist_file = os.path.join(dist_path, hash)

        if not os.path.isdir(dist_path):
            return 'File not found'
        elif not os.path.isfile(dist_file):
            return 'File not found'
        else:
            os.remove(dist_file)
            if not os.listdir(dist_path):
                shutil.rmtree(dist_path)

