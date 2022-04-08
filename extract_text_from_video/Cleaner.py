import os
import shutil


class Cleaner:
    """
    Cleaner class will take one or two arguments

    filePath: Enter your file path wich you want to delete.
    directoryPath: Enter your directory path wich you want to delete, 
    it will delete that directory and all of its children files.
    """
    def __init__(self, filePath=None, directoryPath=None):
        self.filePath = filePath
        self.directoryPath = directoryPath
        self.clean(filePath=self.filePath, directoryPath=self.directoryPath)

    def clean(self, directoryPath=None, filePath=None):
        try:
            if filePath and (os.path.exists(filePath)):

                print(f"[INFO] File {filePath} cleaning...")
                os.remove(filePath)
                print("[INFO] Done.")
                return

            elif(filePath and filePath!=None):
                print(f"[ERROR] {filePath} Does not exist.")

            if directoryPath and (os.path.exists(directoryPath)):
                print(
                    f"[INFO] Delete directory ({directoryPath}) and all its contents..."
                )
                shutil.rmtree(directoryPath)
                print("[INFO] Done.")
                return

            elif(directoryPath and directoryPath!=None):
                print(f"[ERROR] {directoryPath} Does not exist.")

        except Exception as e:
            print(f"[ERROR] {e}")
