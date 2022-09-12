import yaml
from kfp import components, dsl
from kfp.v2 import compiler

def compile_pipeline(cfg):
    @dsl.pipeline(
        name=cfg["name"],
        description=cfg["description"],
        pipeline_root=cfg["gsc_uri"],
    )
    def pipeline(
        experiment:str = cfg["experiment"],
        ) -> None:
        preprocess_op = components.load_component_from_file(cfg["data_prepare_config_path"])
        preprocess_task = preprocess_op()

        train_op = components.load_component_from_file(cfg["train_config_path"])
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
                            "machineType": cfg["machineType"],
                            "acceleratorType": cfg["acceleratorType"],
                            "acceleratorCount": cfg["acceleratorCount"],
                        },
                        "replicaCount": cfg["replicaCount"],
                    }
                ],
            },
        }
    
    compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=cfg["template_path"],
    )

def main():
    with open("configs/pipeline_local.yaml") as f:
        cfg = yaml.safe_load(f)
    compile_pipeline(cfg)
    

if __name__ == "__main__":
    main()
