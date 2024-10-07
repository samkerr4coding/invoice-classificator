import logging
import os
import shutil


class FolderCleaner:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    async def clean(self):
        if os.path.exists(self.folder_path):
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    logging.info(f"Deleted {file_path}")
                except Exception as e:
                    logging.error(f"Failed to delete {file_path}. Reason: {e}")
        else:
            os.makedirs(self.folder_path)
            logging.info(f"Created folder: {self.folder_path}")