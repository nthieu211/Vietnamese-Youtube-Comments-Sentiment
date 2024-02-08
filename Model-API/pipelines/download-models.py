import os
import boto3
from dotenv import load_dotenv
import py_vncorenlp

dest_dir = "model-weight"
file_keys = ["model-metadata.json", "sentiment-model.pth"]

BASE_DIR = os.getcwd()
path_to_dotenv = os.path.join(BASE_DIR, ".env")
load_dotenv(path_to_dotenv)

dest_path = os.path.join(BASE_DIR, dest_dir)
session = boto3.session.Session()
bucket_name = os.environ.get("BUCKET_NAME")
region_name = os.environ.get("REGION_NAME")
endpoint_url = os.environ.get("ENDPOINT_URL") or None
if not os.environ.get("DO_SPACES_ACCESS_KEY") or not os.environ.get(
    "DO_SPACES_SECRET_KEY"
):
    raise Exception(
        "DO_SPACES_ACCESS_KEY and DO_SPACES_SECRET_KEY are required environment variables."
    )
if not bucket_name or not region_name:
    raise Exception("BUCKET_NAME and REGION_NAME are required environment variables.")
client = boto3.client(
    "s3",
    region_name=region_name,
    endpoint_url=endpoint_url,
    aws_access_key_id=os.environ.get("DO_SPACES_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("DO_SPACES_SECRET_KEY"),
    config=boto3.session.Config(
        signature_version="s3v4",
        retries={"max_attempts": 2, "mode": "standard"},
        s3={"addressing_style": "virtual"},
    ),
)
print(f"Downloading files...")
for x in file_keys:
    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    download_path = os.path.join(dest_path, x)
    if not os.path.exists(download_path):
        print(f"Download file: {download_path}")
        client.download_file(Bucket=bucket_name, Key=x, Filename=str(download_path))

# Download vncorenlp
vncorenlp_path = os.path.join(BASE_DIR, "app", "utils", "vncorenlp")
if not os.path.exists(os.path.join(vncorenlp_path, "VnCoreNLP-1.2.jar")):
    print("Downloading vncorenlp...")
    os.makedirs(vncorenlp_path, exist_ok=True)
    py_vncorenlp.download_model(save_dir=vncorenlp_path)
    print(f"Downloaded vncorenlp at {vncorenlp_path}")
