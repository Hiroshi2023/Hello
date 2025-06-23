from huggingface_hub import HfApi, login
import os
import shutil

login(token=os.getenv("HF_API_KEY"))
repo_id = "ton-utilisateur/diamond-model"
local_model_path = "models/"

api = HfApi()
api.create_repo(repo_id, exist_ok=True)
api.upload_folder(
    folder_path=local_model_path,
    repo_id=repo_id,
    repo_type="model"
)
