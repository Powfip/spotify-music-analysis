import os
from pathlib import Path
import kagglehub
import shutil

# -------------------------
# 📁 RUTAS DINÁMICAS
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# 📥 DESCARGA DATASET DE KAGGLE
# -------------------------
dataset_name = 'maharshipandya/-spotify-tracks-dataset'
print(f"Descargando dataset de Kaggle: {dataset_name} ...")

download_dir = kagglehub.dataset_download(dataset_name)  # ahora devuelve un directorio
print(f"Descargado en: {download_dir}")

# -------------------------
# 📂 BUSCAR CSV Y MOVERLO A data/raw
# -------------------------
csv_files = list(Path(download_dir).glob("*.csv"))
if not csv_files:
    raise FileNotFoundError("No se encontró ningún CSV en el dataset descargado")

# Tomamos el primer CSV encontrado y lo renombramos a spotify_raw.csv
shutil.copy(csv_files[0], RAW_DIR / "spotify_raw.csv")

print(f"✅ Dataset disponible en: {RAW_DIR / 'spotify_raw.csv'}")