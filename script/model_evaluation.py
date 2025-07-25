import torch
import json
import os
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from script.model_training import DiamondPricePredictor, prepare_data
from script.data_processing import load_data, preprocess_data

def evaluate_model(model_path, data_path):
    """Évalue le modèle sur les données de test"""
    # Chargement des données
    data = load_data(data_path)
    data = preprocess_data(data)

    os.makedirs('metrics',exist_ok=True)
    # Préparation des données
    X_train, X_test, y_train, y_test = prepare_data(data)
    
    # Chargement du modèle
    model = DiamondPricePredictor(X_train.shape[1])
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))  # Force le chargement sur CPU
    model.eval()
    
    # Assure que toutes les opérations sont sur CPU
    device = torch.device('cpu')
    model = model.to(device)
    X_test = X_test.to(device)
    y_test = y_test.to(device)
    
    # Prédictions
    with torch.no_grad():
        y_pred = model(X_test).cpu().numpy()  # Conversion explicite en numpy array
    
    # Conversion des tenseurs en numpy arrays si nécessaire
    if torch.is_tensor(y_test):
        y_test = y_test.cpu().numpy()
    
    # Calcul des métriques
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score.: {r2:.2f}")
    metrics = {'r2':r2}
    with open('metrics/metrics.json','w') as f:
        json.dump(metrics,f)
    
    return mse, rmse, r2

if __name__ == "__main__":
    evaluate_model('models/diamond_price_predictor.pth', 'data/diamonds.csv')
