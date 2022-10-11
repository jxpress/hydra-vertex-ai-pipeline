# Hydra-Vertex-AI-Pipeline
このレポジトリでは、ML Pipeline のshort introductionとHydraで書かれたコンテナVertex AI Pipelineで実装する具体的な方法とそのサンプルコードを掲載しています。

![training_type](/documents/images/hydra_pipeline_title.png)


<br>


#  📝 ML Pipelineについて
## 👨‍🏭 MLパイプラインとはなにか？

機械学習のトレーニングは、データの前処理、学習、評価等様々なプロセスによって構成されています。
これらのプロセスを、一つのマシーンまたはコンテナで行う学習をMonolith システムと一般的に言われます (図１ (a))。
機械学習を初めて体験するとき、多くの方がこのシステムを利用したと思われます。

一方、機械学習の運用まで考慮したとき、
- データとモデルの再現性の担保 (例 : 学習の度に、ランダム性が含まれる前処理が入ると、結果が変化した要因がつかみにくい)
- プロセスごとに求められるマシーンスペックが異なる (ハイメモリが必要なプロセスもあればGPUが必要なプロセスもある)
- プロセスが独立しているので、使い回しが用意

等の理由から、個々のプロセス (コンポーネントと一般的に呼ばれる)を独立させ処理を行う、Pipelineでの学習が推奨されています (図１ (b))

<br>

ML Pipelineについてのより詳しい情報は [what-a-machine-learning-pipeline-is-and-why-its-important](https://www.datarobot.com/blog/what-a-machine-learning-pipeline-is-and-why-its-important/)や[Full Stack Deep Learning](https://fullstackdeeplearning.com/course/2022/lecture-4-data-management/)を御覧ください。

また、Googleの[ブログ (Rules of Machine Learning:Best Practices for ML Engineering)](https://developers.google.com/machine-learning/guides/rules-of-ml?hl=en)は、学習はPipelineの利用が前提に書かれています。


<br>


![train_type](/documents/images/hydrapipeline_train_type.png)
<p align = "center">
図1 学習システム。 (a)Monolith システムでは、前処理や学習、評価等のプロセスをすべて、同じマシーンまたはコンテナで行う。(b) Pipelineシステムでは、各プロセスを分け独立したリソースで実行する。各プロセスは一般的にコンポーネントと呼ばれている。Pipeline システムでは、コンポーネント間のデータは外部のStrageやDBを経由して行われる。
</p>



<br>

## 💻 Vertex AI pipelineとはなにか？

トレーニングをコンポーネントに分け、それぞれを違うスペックのマシーンで実行するシステムをスクラッチから構築することを想像してみると、非常に複雑であることが想像できると思います。
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

#  HydraとVertex AI Pipeline
[Hydra](https://hydra.cc/)はハイパーパラメーター管理のライブラリとして、非常に素晴らしく、この[例](https://github.com/ashleve/lightning-hydra-template)のように様々な学習コードの取り組まれています。
一方、Hydraで記載されたコンテナを、Vertex AI Pipelineのコンポーネントとして利用しようとした場合、問題が発生します。
## 😖 Problem
Vertex AIでは、各コンポーネントにわたす引数を、yamlファイルのargsで定義します。
この際、[Vertex AIの公式の書き方](https://cloud.google.com/vertex-ai/docs/pipelines/build-own-components)では
```yaml
    command: [python3, main.py]
    args: [
      --project, {inputValue: project},
    ]
```
のように記述する必要があり、以下のように、`argparse`形式のコマンドがコンテナに渡されます。
```bash
python3 main.py --project <value of project>
```

一方、Hydraを用いたコンテナには
```bash
python3 main.py project=<value of project>
```
の形式でコマンドを引き渡す必要があり、工夫無しで実行するとエラーになります。


## 💡 Solution

yamlファイルの書き方を
```yaml
    command: [python3, main.py]
    args: [
      'project={{$.inputs.parameters["project"]}}',
    ]
```
に変更する必要があります。一般的に利用される引数と、それに対応する変換方法は表１に掲載しています。 (例は[こちら](/configs/components/train.yaml))


<br>



表１ : Vertex AIで推奨されている引数の渡し方をHydra用変換する対応表

|  Recommended writing style  |  How to rewrite for Hydra  |
| ---- | ---- |
|   --input-val, {inputValue: Input_name}  |  input-val={{$.inputs.parameters['Input_name']}}  |
|   --input-path, {inputPath: Input_path_name}  |  input-path={{$.inputs.artifacts['Input_path_name'].path}}  |
|   --output-path, {outputPath: Output_path_name}  |  output-path={{$.inputs.artifacts['Output_path_name'].path}}  |


![command error](/documents/images/command.png)


<p align = "center">
図3 YAMLファイルのコマンドを修正する理由と方法の概要図. Hydraで書かれたで公式のコーディングスタイルを使用するとエラーが発生します。エラーを回避するためには、コードを書き換える必要があります。
</p>



<br>


<br>



# 🚀 How to use this repository
このサンプルレポジトリはMNISTの分類するAIの学習を行います。Pipelineは、
- data prepare : MNISTのデータをダウンロードする
- train : 学習を行う
の２つのコンポーネントから構成されます。

![](/documents/images/screen_shot_pipeline.png) #TODO ここを変える
## ✅ step1. componentの作成とArtifact Registryへpush
- Artifact RegistryにpushするURIをそれぞれ決め、それをMakefileのpush-data-prepare-imageとpush-train-imageに書き込みます。

- その後、本レポジトリのroot ディレクトリにて、
```bash
make push-data-prepare-image
make push-train-image
```
をタイプすると、２つのコンポーネントがのビルドとpushがされます。

※ sample codeではdata prepareのdocker imageは本レポジトリの[components/data_prepare](/components/data_prepare)で作成、trainは[Hydraで書かれた学習コード](https://github.com/jxpress/lightning-hydra-template-vertex-ai)で作成し、Artifact Registryにpushすることを想定しています。

## ✅ step2. Building python environment
以下のコマンドをroot folderで入力することでpythonの環境が構築されます。
```bash
make build-python-environment
```

## ✅ step3. Compile Vertex AI pipeline system
1. step1で作成した URIを[data_prepare.yaml](configs/components/data_prepare.yaml) と [train.yaml](configs/components/train.yaml)のimplementation.container.imageに書き足します。
2.[pipeline.yaml](configs/pipeline.yaml)にあなたのGCPのアカウントの情報を加える
3. 以下のコマンドをroot folderで入力することでpipelineがコンパイルされ、`vertex-pipelines-sample.json`が生成されます。
```bash
poetry run python pipeline.py
```


## ✅ step4. Run Vertex AI Pipeline on GCP
コンパイルしたPipelineをGCPで実行するには以下の２つの方法があります。

### 1.  GCPのコンソールに生成されたJSONを提出する
1. [the console of Pipeline](https://console.cloud.google.com/vertex-ai/pipelines/runs)にアクセスします。
2. 画面上部の`CREATE RUN`をクリックします。

![CREATE_RUN](/documents/images/CREATE_RUN.png)


3. 現れた画面で`Pipeline` と `Upload file`をクリックし、さきほど作成した`vertex-pipelines-sample.json`を選択しアップロードします。

![create_pipeline_run](/documents/images/create_pipeline_run.png)

4. `SUBMIT` をクリックすることでPipelineが実行されます。

### 2.Pythonを用いてJSONを提出する
以下のコマンドをroot folderで入力することでPythonを経由で`vertex-pipelines-sample.json`をGCPに提出する事ができます
```bash
poetry run python submit_pipeline_job.py
```
