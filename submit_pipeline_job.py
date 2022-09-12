import json
from ctypes import Union
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import yaml
from google.cloud import aiplatform
from kfp.v2 import compiler

from pipeline import pipeline


def main(
    template_path: Path,
    gcp_region: str,
    gcp_project_id: str,
    name: str,
    compile_pipeline: bool = True,
    *args,
    **kwargs,
):
    if compile_pipeline or not template_path.exists():
        compiler.Compiler().compile(
            pipeline_func=pipeline, package_path=str(template_path)
        )
    display_name = name + "-" + datetime.now().strftime("%Y%m%d%H%M%S")

    job = aiplatform.PipelineJob(
        display_name=display_name,
        template_path=str(template_path),
        location=gcp_region,
        project=gcp_project_id,
    )
    job.submit()


if __name__ == "__main__":
    import yaml

    with open("configs/pipeline_local.yaml") as f:
        cfg = yaml.safe_load(f)
    main(**cfg)
