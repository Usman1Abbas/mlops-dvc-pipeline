# MLOps Kubeflow Assignment

## Project Overview
This project implements a complete MLOps pipeline for the California Housing dataset using Kubeflow Pipelines, DVC, and Jenkins.
The pipeline includes data loading, preprocessing, model training (Random Forest), and evaluation.

## Setup Instructions

### Prerequisites
- Minikube
- Kubeflow Pipelines
- Python 3.9+
- DVC

### Minikube & Kubeflow Setup
1. Install Minikube: `minikube start`
2. Deploy Kubeflow Pipelines: Follow the [official documentation](https://www.kubeflow.org/docs/components/pipelines/v1/installation/localcluster-deployment/)
3. Access KFP Dashboard: `kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80`

### DVC Setup
1. Initialize DVC: `dvc init`
2. Setup remote: `dvc remote add -d myremote /path/to/storage`
3. Pull data: `dvc pull`

## Pipeline Walkthrough

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Compile components:
   ```bash
   python src/pipeline_components.py
   ```

3. Compile pipeline:
   ```bash
   python pipeline.py
   ```

4. Upload `pipeline.yaml` to the Kubeflow Pipelines UI and create a run.
