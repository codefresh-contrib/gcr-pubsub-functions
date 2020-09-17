We will create a GCP Pub/Sub topic named "gcr", and configure a Google Cloud Function to be triggered off of messages from that topic.

Setup:
1. [Create GCP Pub/Sub topic for GCR](https://cloud.google.com/container-registry/docs/configuring-notifications)
1. Select the TRIGGER CLOUD FUNCTION option.
1. Create Function `run-codefresh-pipeline`
1. Expand VARIABLES and input this variable `CODEFRESH_API_KEY` with a key with pipeline read/run scope.
1. Move on to Code 
1. Runtime: Python 3.7
1. Entry point: run_codefresh_pipeline
1. Using the main.py and requirements.txt below create a new function.

Now for your pipeline(s) you want to be triggered add a new pipeline tag via [Pipeline Settings](https://codefresh.io/docs/docs/configure-ci-cd-pipeline/pipelines/#pipeline-settings) with the name or a specific tag of the image pushed to GCR.

The function will lookup all tags and when one is found matching the tag of the GCR Pub/Sub trigger it will trigger a build of that Codefresh pipeline.

As you add more pipelines tag them with the GCR image names that will trigger them and they can all share this function.
