push-data-prepare-image: ## build and push Docker image of data_prepare. Replace uri whatever you want
	docker build components/data_prepare/ -t <uri of GCP artifact repository>:<tag>
	docker push <uri of GCP artifact repository>:<tag>

push-train-image: ## build and push Docker image of train. Replace uri whatever you want
	git clone git@github.com:jxpress/lightning-hydra-template-vertex-ai.git
	cd lightning-hydra-template-vertex-ai
	docker build . -t <uri of GCP artifact repository>:<tag>
	docker push <uri of GCP artifact repository>:<tag>

compile-pipeline-yaml: ## create yaml file for excecuting pipeline of Vertex AI
	poetry run python pipeline.py

compile-and-submit-pipeline-yaml: ## create and submit yaml file for excecuting pipeline of Vertex AI
	poetry run python submit_pipeline_job.py
