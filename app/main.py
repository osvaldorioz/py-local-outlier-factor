from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import numpy as np
from typing import List
import matplotlib
import matplotlib.pyplot as plt
import torch
import lof
import json

matplotlib.use('Agg')  # Usar backend no interactivo
app = FastAPI()

# Definir el modelo para el vector
class VectorF(BaseModel):
    vector: List[float]
    
@app.post("/local-outlier-factor")
def calculo(data_size: int):
    output_file = 'local_outlier_factor.png'
    # Generar datos normales
    np.random.seed(42)
    normal_data = np.random.randn(data_size, 2) * 0.5

    # Agregar anomalías
    anomalies = np.random.uniform(low=-3, high=3, size=(5, 2))

    # Unir datos normales y anomalías
    data = np.vstack([normal_data, anomalies])
    data_tensor = torch.tensor(data, dtype=torch.float32)

    # Ejecutar el algoritmo LOF en C++
    lof_scores = lof.local_outlier_factor(data_tensor, k=5).numpy()

    # Definir umbral para anomalías
    threshold = np.percentile(lof_scores, 90)  # Top 10% de LOF son anomalías
    anomaly_indices = np.where(lof_scores > threshold)[0]

    # Graficar los resultados
    plt.figure(figsize=(8, 6))
    plt.scatter(data[:, 0], data[:, 1], c="blue", label="Normal")
    plt.scatter(data[anomaly_indices, 0], data[anomaly_indices, 1], c="red", label="Anomalía", edgecolors="black", s=100)
    plt.legend()
    plt.title("Detección de Anomalías con LOF") 
    #plt.show()
    plt.savefig(output_file)
    plt.close()
    
    j1 = {
        "Grafica": output_file
    }
    jj = json.dumps(str(j1))

    return jj

@app.get("/local-outlier-factor-graph")
def getGraph(output_file: str):
    return FileResponse(output_file, media_type="image/png", filename=output_file)