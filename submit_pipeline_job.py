from datetime import datetime
from os.path import exists

import yaml
from google.cloud import aiplatform
from pipeline import main as create_json


def main(
    cfg:dict
):
    if cfg["compile_pipeline"] or not exists(cfg["template_path"]):
        create_json()
    display_name = cfg["name"] + "-" + datetime.now().strftime("%Y%m%d%H%M%S")

    job = aiplatform.PipelineJob(
        display_name=display_name,
        template_path=cfg["template_path"],
        location=cfg["gcp_region"],
        project=cfg["gcp_project_id"],
    )
    job.submit()


if __name__ == "__main__":
    import yaml

    with open("configs/pipeline_local.yaml") as f:
        cfg = yaml.safe_load(f)
    main(cfg)
