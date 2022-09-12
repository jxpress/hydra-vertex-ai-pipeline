import yaml
from kfp import components, dsl
from kfp.v2 import compiler

with open("configs/pipeline.yaml") as f:
    cfg = yaml.safe_load(f)


@dsl.pipeline(
    name=cfg["name"],
    description=cfg["description"],
    pipeline_root=cfg["gsc_uri"],
)
def pipeline(
    # preprocess
    # train
    experiment: str = cfg["experiment"],
) -> None:
    preprocess_op = components.load_component_from_file("configs/data_prepare.yaml")
    preprocess_task = preprocess_op()

    train_op = components.load_component_from_file("configs/train.yaml")
    train_task = train_op(
        data_dir=preprocess_task.outputs["data_dir"],
        experiment=experiment,
    )
    train_task.custom_job_spec = {
        "displayName": train_task.name,
        "jobSpec": {
            "workerPoolSpecs": [
                {
                    "containerSpec": {
                        "imageUri": train_task.container.image,
                        "command": train_task.command,
                        "args": train_task.arguments,
                    },
                    "machineSpec": {
                        "machineType": "n1-standard-4",
                        "acceleratorType": "NVIDIA_TESLA_T4",
                        "acceleratorCount": 1,
                    },
                    "replicaCount": 1,
                }
            ],
        },
    }


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=cfg["template_path"],
    )
