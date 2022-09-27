from logging import getLogger

import functions
import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

log = getLogger(__name__)


@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: DictConfig):
    log.info("##config##\n" + OmegaConf.to_yaml(cfg))
    for _, function in cfg.functions.items():
        if isinstance(function, DictConfig) and "_target_" in function:
            log.info(f"Processing {function._target_}")
            function = instantiate(function)
            function.run()

if __name__ == "__main__":
    main()
