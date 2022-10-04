# Hydra-Vertex-AI-Pipeline

![training_type](/documents/images/hydra_pipeline_title.png)


<br>


#  📝 ML Pipelineについて
## 👨‍🏭 MLパイプラインとはなにか？

機械学習のトレーニングは、データの前処理、学習、評価等様々なプロセスによって構成されています。
これらのプロセスを一つのマシーンまたは、コンテナで行う学習をMonolith システムと一般的に言われます (図１ (a))。
機械学習を初めて体験するとき、多くの方がこのシステムを利用したと思われます。

一方、機械学習の運用まで考慮したとき、
- データとモデルの再現性の担保 (例 : 学習の度に、ランダム性が含まれる前処理が入ると、結果が変化した要因がつかみにくい)
- プロセスごとに求められるマシーンスペックが異なる (ハイメモリが必要なプロセスもあればGPUが必要なプロセスもある)
- プロセスが独立しているので、使い回しが用意
等の理由から、個々のプロセス (コンポーネントと一般的に呼ばれる)を独立させ処理を行う、Pipelineでの学習が推奨されています (図１ (b))

<br>

![train_type](/documents/images/hydrapipeline_train_type.png)
<p align = "center">
図1 学習システム。 (a)Monolith システムでは、前処理や学習、評価等のプロセスをすべて同じマシーン、またはコンテナで行う。(b) Pipelineシステムでは、各プロセスを分け独立したリソースで実行する。各プロセスは一般的にコンポーネントと呼ばれている。Pipeline システムでは、コンポーネント間のデータは外部のStrageやDBを経由して行われる。
</p>


<br>


詳しくは [what-a-machine-learning-pipeline-is-and-why-its-important](https://www.datarobot.com/blog/what-a-machine-learning-pipeline-is-and-why-its-important/)や[Full Stack Deep Learning](https://fullstackdeeplearning.com/course/2022/lecture-4-data-management/)を御覧ください。

また、Googleの[ブログ (Rules of Machine Learning:Best Practices for ML Engineering)](https://developers.google.com/machine-learning/guides/rules-of-ml?hl=en)は、学習はPipelineの利用が前提に書かれています。

<br>

## 💻 Vertex AI pipelineとはなにか？


Pipelineのメリットを享受するために、トレーニングをコンポーネントに分け、それぞれを違うスペックのマシーンで実行するシステムをスクラッチから構築することを想像してみてください。非常に複雑であることが想像できると思います。

一方、Vertex AI Pipelineを利用することで、図2に示すようにGCPの他のサービスと連携しながらML Pipelineを容易に構築することができます

![Intro_vertex_ai_pipeline](/documents/images/Intro_vertex_ai_pipeline.png)
<p align = "center">
図2 Vertex AI Pipelineのシステム例。 Docker ImageはArtifact RegistryやContainer Registryで管理し、各コンポーネントはGCE等のリソースを用いて処理する。学習データやAIモデル等ははGoogle Strageに保存ができる。Vertex AI Pipelineを用いることで、これらのGCPサービスと連携しながらML Pipeline構築を容易に行うことができる。
</p>

Vertex AI Pipeline のその他メリットやより詳細な部分については、以下の素晴らしいブログをご確認ください
- [Google公式のドキュメント](https://cloud.google.com/vertex-ai/docs/pipelines/)
- 杉山様の[ブログ](https://tech.repro.io/entry/2021/06/22/125113)と[サンプルコード](https://github.com/reproio/lab_sample_pipelines)
- Tonouchi様の[ブログ](https://team-blog.mitene.us/kubeflow-pipelines-design-pattern-e5ced1a4dd44)と[サンプルコード](https://github.com/tonouchi510/kfp-project)


Vertex AIを用いることで、ML Pipelineの構築が楽に行えることが体験できると思います。


<br>

## 😖hydraとVertex AI Pipelineの問題点
各コンポーネントにわたす引数を
## 解決法

# how to use
## step1. componentの作成とartificial registoryへpush
## step2. componentをつなぐ
## step3. Run it on Vertex AI

# further information
## valueとpath以外の書き方 :わからないことがあった場合