import os
import shutil


class Cleaner:
    def __init__(self, filePath):
        self.filePath = filePath
        self.cleaner(self.filePath)

    def cleaner(self, filePath=None, directoryPath=None):
        try:
            if filePath and (os.path.exists(filePath)):

                print(f"[INFO] File {filePath} cleaning...")
                os.remove(filePath)
                print("[INFO] Done.")
                return
            else:
                print(f"[ERROR] {filePath} Does not exist.")

            if directoryPath and (os.path.exists(directoryPath)):
                print(
                    f"[INFO] Deletes a directory ({directoryPath}) and all its contents..."
                )
                shutil.rmtree(directoryPath)
                print("[INFO] Done.")
                return
            else:
                print(f"[ERROR] {directoryPath} Does not exist.")

        except Exception as e:
            print(f"[ERROR] {e}")
