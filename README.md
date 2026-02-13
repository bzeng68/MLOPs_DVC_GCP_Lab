# Data Version Control (DVC) Lab

## Overview

[DVC](https://dvc.org/) is an open-source tool for data versioning in machine learning projects. It allows you to track changes in datasets over time (similar to how git is version control for code), ensuring reproducibility and efficient collaboration.

In this lab, you'll learn to use DVC with Google Cloud Storage to version control the Credit Card dataset and build reproducible ML pipelines.

---

## Quick Start (Pipeline Demo)

Once you have the dataset in `data/CC_GENERAL.csv`, try the DVC pipeline:

```bash
# Install dependencies
uv sync

# Create the pipeline (see "DVC Pipelines" section below for details)
uv run -m dvc stage add -n preprocess \
    -d data/CC_GENERAL.csv \
    -o data/processed.csv \
    uv run scripts/preprocess.py

uv run -m dvc stage add -n train \
    -d data/processed.csv \
    -o models/model.pkl \
    -M metrics.json \
    uv run scripts/train.py

# Run the pipeline
uv run -m dvc repro

# Visualize it
uv run -m dvc dag

# View metrics
uv run -m dvc metrics show
```

---

## Setup

### 1. Create Google Cloud Storage Bucket

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project for this lab
3. Navigate to **Cloud Storage** → **Buckets** → **Create Bucket**
4. Configure settings:
   - Name: Choose a unique bucket name
   - Region: `us-east1`
   - Storage class: Standard
5. Click **Create**

### 2. Create Service Account Credentials

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. Name: `dvc-lab`, Role: **Storage Object Admin**
4. Click **Create and Continue** → **Done**
5. Select the service account → **Keys** tab → **Add Key** → **Create new key**
6. Download the JSON credentials file and save securely

**Make sure to not commit your secrets file.**

---

## Installation & Configuration

### Install UV Package Manager and Initialize
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init
```

### Install DVC
```bash
uv install dvc
uv install dvc-gs
uv sync
```

### Initialize DVC

```bash
uv run -m dvc init
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

### Configure Remote Storage

```bash
# Add remote (replace with your bucket name)
uv run -m dvc remote add -d myremote gs://<your-bucket-name>

# Set credentials path
uv run -m dvc remote modify myremote credentialpath <path-to-json-credentials>
```

Your `.dvc/config` will look like:
```ini
[core]
    remote = myremote
['remote "myremote"']
    url = gs://<your-bucket-name>
    credentialpath = /path/to/credentials.json
```

---

## Tracking Data

### Download Dataset

Download the [Credit Card Dataset](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata) and place it in the `data/` folder as `CC_GENERAL.csv`.

### Add Data to DVC

```bash
# Track the dataset
uv run -m dvc add data/CC_GENERAL.csv

# This creates:
# - data/CC_GENERAL.csv.dvc (metadata - commit to Git)
# - data/.gitignore (excludes actual data from Git)

# Commit to Git
git add data/CC_GENERAL.csv.dvc data/.gitignore
git commit -m "Track CC_GENERAL.csv with DVC"

# Push data to remote storage
uv run -m dvc push
```

---

## Working with Versions

### Update Dataset

When you modify the dataset:

```bash
# Update DVC tracking (computes new hash)
uv run -m dvc add data/CC_GENERAL.csv

# Commit changes
git add data/CC_GENERAL.csv.dvc
git commit -m "Update dataset: description of changes"

# Push to remote
uv run -m dvc push
```

### Revert to Previous Version

```bash
# View Git history
git log --oneline

# Checkout previous commit
git checkout <commit-hash> data/CC_GENERAL.csv.dvc

# Retrieve corresponding data version
uv run -m dvc checkout
```

**Using Git tags:**
```bash
# Tag versions
git tag -a v1.0 -m "Initial dataset"

# Revert to tag
git checkout v1.0 data/CC_GENERAL.csv.dvc
uv run -m dvc checkout
```

### Pull Data on New Machine

```bash
git clone <repo-url>
cd <repo-name>
uv run -m dvc pull
```

---

## DVC Pipelines - Reproducible ML Workflows

DVC pipelines automate your ML workflow by defining stages with dependencies and outputs. Each stage only re-runs when its dependencies or content change. The entire workflow will not be run unless manually done or every stage of the workflow is modified.

### Pipeline Structure

Our pipeline has two stages:

1. **Preprocess**: Clean raw data and handle missing values
2. **Train**: Train K-means clustering model on processed data

### Create the Pipeline

```bash
# Stage 1: Preprocess data
uv run -m dvc stage add -n preprocess \
    -d data/CC_GENERAL.csv \
    -o data/processed.csv \
    uv run scripts/preprocess.py

# Stage 2: Train model
uv run -m dvc stage add -n train \
    -d data/processed.csv \
    -o models/model.pkl \
    -M metrics.json \
    uv run scripts/train.py
```

**Stage options explained:**
- `-n`: Stage name
- `-d`: Dependencies (inputs) - stage re-runs when these change
- `-o`: Outputs - tracked by DVC
- `-M`: Metrics file - for tracking model performance

This creates a `dvc.yaml` file that defines your pipeline and a `dvc.lock` file that tracks exact versions.

### Run the Pipeline

```bash
# Run entire pipeline
uv run -m dvc repro
# can use -f flag to force full rerun without cache

# Visualize pipeline structure
uv run -m dvc dag
```

### View Metrics

```bash
# Show metrics from all pipeline runs
uv run -m dvc metrics show
```

### Modifying the Pipeline

When you change data or code:

```bash
# Re-run pipeline (only changed stages execute)
uv run -m dvc repro

# Commit pipeline changes
git add dvc.yaml dvc.lock
git commit -m "Update pipeline results"

# Push data and model to remote
uv run -m dvc push
```

### Example Output

After running `uv run -m dvc dag`, you'll see:
```
+-------------------------+  
| data/CC_GENERAL.csv.dvc |  
+-------------------------+  
              *              
              *              
              *              
      +------------+         
      | preprocess |         
      +------------+         
              *              
              *              
              *              
         +-------+           
         | train |           
         +-------+ 
```

---

## Common Commands

```bash
dvc add <file>           # Track file with DVC
dvc push                 # Upload data to remote
dvc pull                 # Download data from remote
dvc checkout             # Restore data version
dvc status               # Check synchronization status
dvc repro                # Run/reproduce pipeline
dvc dag                  # Visualize pipeline graph
dvc metrics show         # Display metrics
```

---

## Resources

- [DVC Documentation](https://dvc.org/doc)
- [DVC Pipelines Guide](https://dvc.org/doc/user-guide/pipelines)
- [DVC Tutorial Video](https://www.youtube.com/watch?v=kLKBcPonMYw)
- [Original Lab Reference](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Data_Labs/DVC_Labs/Lab_1)