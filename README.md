# Hydra-Vertex-AI-Pipeline

![training_type](/documents/images/hydra_pipeline_title.png)

This repository focus on `how to run code written in Hydra on the Vertex AI Pipeline`.

- [The first half of the README](#usage) describes **how to use the repository**
- [The second half](#description) provides **a brief description of Vertex Pipeline, compatibility issues with Hydra, and how to resolve them**.

The Japanese blog is [here](https://tech.jxpress.net/entry/2022/10/31/113519)

<br>


<h1 id="usage">🚀 How to use this Repository</h1>
This sample repository shows a pipeline system to classify MNIST.
The pipeline consists of the following two components

- data prepare: download MNIST data
- train: perform training

![pipeline](/documents/images/pipeline_image.png)
## ✅ step1. Build and push Docker Images
- Decide URIs of **data_prepare** and **train** to push to GCP, and write them in the push-data-prepare-image and push-train-image of [Makefile](/Makefile).

- Then, in the root directory of this repository, run
```bash
make push-data-prepare-image
make push-train-image
```
to build and pushed two Docker Images.

※  In the sample code, the Docker Image of the data prepare is built in [components/data_prepare](/components/data_prepare) in this repository.
The process of the data prepare is written by Hydra. In detail, after writing function codes in [functions](/components/data_prepare/functions/), You can determine the functions to be processed as parameters by writing them in [config.yaml](/components/data_prepare/config.yaml), which is a similar way to [manage hyperparameters in AI training](https://github.com/ashleve/lightning-hydra-template).

Also, the Docker Image of the train is from [train code written in Hydra](https://github.com/jxpress/lightning-hydra-template-vertex-ai).

## ✅ step2. Building python environment
Run 
```bash
make build-python-environment
```

## ✅ step3. Compile Vertex AI pipeline system
1. Add the image URIs used in step1 to implementation.container.image of [data_prepare.yaml](configs/components/data_prepare.yaml) and [train.yaml](configs/components/train.yaml).
2. Add information about your GCP account to [pipeline.yaml](configs/pipeline.yaml)
3. Run 
```bash
poetry run python pipeline.py
```

then `vertex-pipelines-sample.json` will be created

## ✅ step4. Run Vertex AI Pipeline on GCP
There are 2 ways to run a pipeline. 

### 1.  Submit JSON file to GCP console.
1. Access [the console of Pipeline](https://console.cloud.google.com/vertex-ai/pipelines/runs)
2. Click `CREATE RUN` at the top of the console screen.

![CREATE_RUN](/documents/images/CREATE_RUN.png)


3. Click `Pipeline` and choose `Upload file`. Then upload `vertex-pipelines-sample.json` which was created in step4.

![create_pipeline_run](/documents/images/create_pipeline_run.png)

4. Click `SUBMIT` to run the pipeline.

### 2. Submit JSON file via python.
Run the following command
```bash
poetry run python submit_pipeline_job.py
```

---


<h1 id="description">📝 About the ML Pipeline</h1>

## 👨‍🏭 What is the ML Pipeline?
Training process of Deep Learning usually consists of various processes such as data preprocessing, training, and evaluation.
Training in which these processes are performed on a single machine or container is commonly referred to as a Monolith system (Figure 1 (a)).
I guess many people's first experience with machine learning is likely to have been with this system.

On the other hand, when considering the operation of machine learning, it is important to
- Ensure reproducibility of data and models (e.g., if randomness is included in preprocessing and executed in every training process, it is difficult to find out the factors that changed the results).
- Different processes require different machine specifications (e.g., some processes require high memory while another require GPUs).
- Because the processes are independent, they can be used interchangeably.

For these reasons, using a pipeline is recommended for training, where each process (generally called a component) is processed independently (Figure 1 (b)).


For more information, see [what-a-machine-learning-pipeline-is-and-why-its-important](https://www.datarobot.com/blog/what-a-machine-learning-pipeline-is-and-why-its-important/) or [Full Stack Deep Learning](https://fullstackdeeplearning.com/course/2022/lecture-4-data-management/).

Also see Google's [blog (Rules of Machine Learning: Best Practices for ML Engineering)](https://developers.google.com/machine-learning/guides/rules-of-ml?hl=en) is based on the assumption that Pipeline is used for training.

<br>

![train_type](/documents/images/hydrapipeline_train_type.png)
<p align = "center">
Figure1 Training process of Deep Learning. (a) In a Monolith system, all processes such as preprocessing, training, and evaluation are executed on the same machine or container. (b) In a Pipeline system, each process is separated and executed on independent resources. Each process is generally referred to as a component; in a Pipeline system, data between components is routed through external storage or DB.
</p>



<br>


## 💻 What is Vertex AI pipeline
Let's say imagine building a pipeline system from scratch that divides each training process into components, each running on a different spec machine. You might feel that it would be very complex.

On the other hand, with Vertex AI Pipeline, you can easily build an ML Pipeline in conjunction with other GCP services, as shown in Figure 2.


![Intro_vertex_ai_pipeline](/documents/images/Intro_vertex_ai_pipeline.png)
<p align = "center">
Figure 2  Example of Vertex AI Pipeline system. Docker images are managed in the Artifact Registry, and each component is executed on resources such as GCE. Training data and AI models can be stored in Google Storage. As shown in this figure Vertex AI Pipeline makes it easy to build ML pipelines in conjunction with these GCP services.
</p>

For more information about Vertex AI Pipeline, please see [the official documentation](https://cloud.google.com/vertex-ai/docs/pipelines/).
If you want to know an excellent sample code, please see [this sample code](https://github.com/reproio/lab_sample_pipelines), which is truly excellent for starting the Vertex AI Pipeline.


# Hydra and Vertex AI Pipeline
[Hydra](https://hydra.cc/) is an excellent library for hyperparameter management.
Various training codes have been written, as in [this example](https://github.com/ashleve/lightning-hydra-template).
On the other hand, problems arise when trying to use containers written in Hydra as components of the Vertex AI Pipeline.

## 😖 Problem
In Vertex AI Pipeline, the arguments to be passed to each component are defined in the args of the YAML file.
According to [the official document of Vertex AI](https://cloud.google.com/vertex-ai/docs/pipelines/build-own-components), it is necessary to write like the below.

```yaml
    command: [python3, main.py]
    args: [
      --project, {inputValue: project},
    ]
```

this leads following command being passed to the container

```bash
python3 main.py --project <value of project>
```


However, passing commands in this format to a container using Hydra will result in an error (Figure 3).
This is because the code written in Hydra requires the command to be passed in the following format

```bash
python3 main.py project=<value of project>
```
## 💡 Solution
The coding style of the YAML file needs to be changed as follows (Figure 3).
```yaml
    command: [python3, main.py]
    args: [
      'project={{$.inputs.parameters["project"]}}',
    ]
```


Commonly used arguments and the corresponding conversion methods are listed in Table 1. 

Table 1: Correspondence table for converting the recommended argument passing in Vertex AI for Hydra.
|  Official coding style  |  How to rewrite for Hydra  |
| ---- | ---- |
|   --input-val, {inputValue: Input_name}  |  input-val={{$.inputs.parameters['Input_name']}}  |
|   --input-path, {inputPath: Input_path_name}  |  input-path={{$.inputs.artifacts['Input_path_name'].path}}  |
|   --output-path, {outputPath: Output_path_name}  |  output-path={{$.inputs.artifacts['Output_path_name'].path}}  |


![command error](/documents/images/command.png)


<p align = "center">
Figure3 Schematic Diagram of why and how to modify commands in the YAML file. a container is written Hydra generates an error if using the Official coding style. To avoid errors, the code must be rewritten.
</p>




<br>


<br>

