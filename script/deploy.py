from huggingface_hub import HfApi, login
import os

def deploy_model():
    token = os.getenv("HF_API_KEY")
    if not token:
        raise ValueError("Le token Hugging Face est manquant. Définissez la variable d’environnement HF_API_KEY.")
    
    login(token=token)

    repo_id = "Hiroshi99/diamond-model"
    local_model_path = "models/"

    api = HfApi()
    api.create_repo(repo_id, exist_ok=True)
    api.upload_folder(
        folder_path=local_model_path,
        repo_id=repo_id,
        repo_type="model"
    )
    print(f"Modèle déployé avec succès sur {repo_id}")

if __name__ == "__main__":
    deploy_model()
