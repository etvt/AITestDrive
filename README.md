`aitestdrive` local start instructions:

1. Install gcloud-sdk.
2. `gcloud auth application-default login`
3. `gcloud config set project <project-id>`
4. Copy `.env.example` to `.env` and provide the required values.
5. Run the server (use `poetry run server` or one of the provided PyCharm run-configurations).
