push-data-prepare-image: ## build and push Docker image of data_prepare
	docker build components/data_prepare/ -t <uri of GCP artifact repository>:<tag> ## you can replace it whatever you want 
	docker push <uri of GCP artifact repository>:<tag> ## you can replace it whatever you want
