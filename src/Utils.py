import psutil

class Utils:
    @staticmethod
    def checkRamSize():
       return psutil.virtual_memory().total/(1024**3) > 18.0
