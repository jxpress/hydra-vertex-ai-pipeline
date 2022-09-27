__version__ = "0.1.0"

from torchvision.datasets import MNIST

class DownloadData():
    def __init__(self, root:str,train:bool, download:bool):
        self.root = root
        self.train = train
        self.download = download
        
    def __call__(self,):
        MNIST(
            root = self.root,
            train = self.train,
            download = self.download, 
        )
        
    def run(self):
        self.__call__()