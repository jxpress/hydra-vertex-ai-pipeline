push-data-prepare-image: ## build and push Docker image of data_prepare. Replace uri whatever you want
	docker build components/data_prepare/ -t <uri of GCP artifact repository>:<tag>
	docker push <uri of GCP artifact repository>:<tag>

push-train-image: ## build and push Docker image of train. Replace uri whatever you want
	rm -rf lightning-hydra-template-vertex-ai
	git clone git@github.com:jxpress/lightning-hydra-template-vertex-ai.git
	docker build lightning-hydra-template-vertex-ai/ -t <uri of GCP artifact repository>:<tag>
	docker push <uri of GCP artifact repository>:<tag>

build-python-environment: ## build python environment for compile pipeline
	pip install poetry
	poetry install
