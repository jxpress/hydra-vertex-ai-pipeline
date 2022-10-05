# Hydra-Vertex-AI-Pipeline

![training_type](/documents/images/hydra_pipeline_title.png)


<br>


#  📝 Abour the ML Pipeline
## 👨‍🏭 What is the ML Pipeline?
Training process of Deep Learning usually consists of various processes such as data preprocessing, training, and evaluation.
Training in which these processes are performed on a single machine or container is commonly referred to as a Monolith system (Figure 1 (a)).
I guess many people's first experience with machine learning is likely to have been with this system.

On the other hand, when considering the operation of machine learning, it is important to
- Ensure reproducibility of data and models (e.g., if randomness is included in preprocessing and executed in every training process, it is difficult to find out the factors that changed the results).
- Different processes require different machine specifications (e.g., some processes require high memory while another require GPUs).
- Because the processes are independent, they can be used interchangeably.
For these reasons, using pipeline is recommended for training, where each process (generally called a component) is processed independently (Figure 1 (b)).


<br>

![train_type](/documents/images/hydrapipeline_train_type.png)
<p align = "center">
Figure1 Training process of Deep Learning. (a) In a Monolith system, all processes such as preprocessing, training, and evaluation are executed on the same machine or container. (b) In a Pipeline system, each process is separated and executed on independent resources. Each process is generally referred to as a component; in a Pipeline system, data between components is routed through an external storage or DB.
</p>

For more information, see [what-a-machine-learning-pipeline-is-and-why-its-important](https://www.datarobot.com/blog/what-a-machine-learning-pipeline-is-and-why-its-important/) or [Full Stack Deep Learning](https://fullstackdeeplearning.com/course/2022/lecture-4-data-management/).

Also see Google's [blog (Rules of Machine Learning:Best Practices for ML Engineering)](https://developers.google.com/machine-learning/guides/rules-of-ml?hl=en) is based on the assumption that Pipeline is used for training.


<br>


## 💻 what is Vertex AI pipeline
Let's say imagine building a pipeline system from scratch that divides training process into components, each running on a different spec machine. You might feel that it would be very complex.

On the other hand, with Vertex AI Pipeline, you can easily build an ML Pipeline in conjunction with other GCP services, as shown in Figure 2.


![Intro_vertex_ai_pipeline](/documents/images/Intro_vertex_ai_pipeline.png)
<p align = "center">
Figure 2  Vertex AI Pipeline system example. Docker images are managed in the Artifact Registry and Container Registry, and each component is processed using resources such as GCE. Training data and AI models can be stored in Google Strage, and Vertex AI Pipeline makes it easy to build ML pipelines in conjunction with these GCP services.
</p>

For more information about Vertex AI Pipeline, please see [official documentation](https://cloud.google.com/vertex-ai/docs/pipelines/).
If you want to know excellent sample code, please see [this sample code](https://github.com/reproio/lab_sample_pipelines), which is truly excellent for starting Vertex AI Pipeline.


# Hydra and Vertex AI Pipeline
[Hydra](https://hydra.cc/) is a excellent library for hyperparameter management.
Various learning codes have been written, as in [this example](https://github.com/ashleve/lightning-hydra-template).
On the other hand, problems arise when trying to use containers written in Hydra as components of the Vertex AI Pipeline.

## 😖 Problem
In Vertex AI Pipeline, the arguments to be passed to each component are defined in the args of the yaml file.
According to [Official document of Vertex AI](https://cloud.google.com/vertex-ai/docs/pipelines/build-own-components), it is necessary to write like below.

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


However, passing commands in this format to a container using Hydra will result in an error.
This is because the code written in Hydra requires the command to be passed in the following format

```bash
python3 main.py project=<value of project>
```
## 💡 Solution
The coding style of the yaml file needs to be changed as follows.
```yaml
    command: [python3, main.py]
    args: [
      'project={{$.inputs.parameters["project"]}}',
    ]
```

Commonly used arguments and the corresponding conversion methods are listed in Table 1. 

Table 1 : Correspondence table for converting the recommended argument passing in Vertex AI for Hydra.
|  Recommended writing style  |  How to rewrite for Hydra  |
| ---- | ---- |
|   --input-val, {inputValue: Input_name}  |  input-val={{$.inputs.parameters['Input_name']}}  |
|   --input-path, {inputPath: Input_path_name}  |  input-path={{$.inputs.artifacts['Input_path_name'].path}}  |
|   --output-path, {outputPath: Output_path_name}  |  output-path={{$.inputs.artifacts['Output_path_name'].path}}  |




<br>


<br>



# 🚀 How to use this 
This sample repository will train an AI to classify MNIST.
Pipeline consists of the following two components
- data prepare : download MNIST data
- train : perform training

## ✅ step1. Build and push Docker Image
- Decide uri of data_prepare and train to push, and write them in the Makefile push-data-prepare-image and push-train-image.

- Then, in the root directory of this repository, run
```bash
make push-data-prepare-image
make push-train-image
```
to built and pushed two Docker Images.

※  In the sample code, the Docker Image for data prepare is build in [components/data_prepare](/components/data_prepare) in this repository and train is build in [train code written in Hydra](https://github.com/jxpress/lightning-hydra-template-vertex-ai).

## ✅ step2. componentをつなぐ
## ✅ step3. Run it on Vertex AI

# further information
## valueとpath以外の書き方 :わからないことがあった場合