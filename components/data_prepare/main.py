from logging import getLogger

import hydra
from omegaconf import DictConfig, OmegaConf
import functions
log = getLogger(__name__)

@hydra.main(version_base=None,config_path=".", config_name="config")
def main(cfg: DictConfig):
    log.info("##config##\n" + OmegaConf.to_yaml(cfg))
    for function in cfg.functions:
        log.info(f"Processing {function._target_}")
        function = OmegaConf.to_container(function, resolve=True)
        func = getattr(functions, function.pop("_target_"))
        func(**function)
    

if __name__ == "__main__":
    main()
