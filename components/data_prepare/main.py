from datetime import datetime
from logging import getLogger
from pathlib import Path

import hydra
from omegaconf import DictConfig
log = getLogger(__name__)
from torchvision.datasets import MNIST

@hydra.main(version_base=None,config_path=".", config_name="config")
def main(cfg: DictConfig):
    MNIST(cfg.data_dir, train=True, download=True)
    MNIST(cfg.data_dir, train=False, download=True)
    

if __name__ == "__main__":
    main()