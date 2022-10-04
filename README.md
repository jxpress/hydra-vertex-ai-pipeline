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


## hydraとVertex AIのpipelineの問題点
## 解決法

# how to use
## step1. componentの作成とartificial registoryへpush
data prepareもhydra likeな書き方を下
## step2. componentをつなぐ
## step3. Run it on Vertex AI

# further information
## valueとpath以外の書き方 :わからないことがあった場合