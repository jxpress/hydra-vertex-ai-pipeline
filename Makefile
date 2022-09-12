push-data-prepare-image: ## build and push Docker image of data_prepare
	docker build components/data_prepare/ -t <uri of GCP artifact repository>:<tag> ## you can replace it whatever you want 
	docker push <uri of GCP artifact repository>:<tag> ## you can replace it whatever you want

compile-pipeline-yaml: ## create yaml file for excecuting pipeline of Vertex AI
	poetry run python pipeline.py

compile-and-submit-pipeline-yaml: ## create and submit yaml file for excecuting pipeline of Vertex AI
	poetry run python submit_pipeline_job.py
