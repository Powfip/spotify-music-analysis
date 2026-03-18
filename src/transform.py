import pandas as pd
from pathlib import Path

# -------------------------
# 📁 RUTAS DINÁMICAS
# -------------------------
BASE_DIR =Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# CARPETAS DEL DATASET CRUDO
RAW_DIR = PROJECT_ROOT / "data" / "raw" 

# RUTA COMPLETA AL CSV
CSV_PATH = RAW_DIR / "Spotify_raw.csv"

# -------------------------
# 📥 CARGAR CSV
# -------------------------
df = pd.read_csv(CSV_PATH)
print(f'✅ CSV cargado: {CSV_PATH}')


# Borrar columnas innecesarias
df = df.drop(columns=["Unnamed: 0", "track_id", "album_name", "key", "mode", 
                       "loudness", "speechiness", "acousticness", 
                       "instrumentalness", "liveness", "time_signature"])


print(df.info())
print(df["track_genre"].unique())  # ver qué géneros hay exactamente
# Mapeo de subgéneros a géneros principales
genre_map = {
    "rock": ["rock", "alt-rock", "alternative", "hard-rock", "punk-rock", 
             "psych-rock", "punk", "grunge", "emo"],
    "pop":  ["pop", "synth-pop", "indie-pop", "power-pop", "k-pop", 
             "j-pop", "cantopop", "mandopop"],
    "rap":  ["hip-hop"],
    "reggaeton": ["reggaeton", "latino"]
}

# Invertir el mapeo para hacer el reemplazo
reverse_map = {subgenre: genre for genre, subgenres in genre_map.items() 
               for subgenre in subgenres}

# Filtrar y renombrar
df = df[df["track_genre"].isin(reverse_map.keys())].copy()
df["track_genre"] = df["track_genre"].map(reverse_map)

print(df["track_genre"].value_counts())
print(f"\nTotal filas: {df.shape[0]}")

df_balanced = pd.concat([
    df[df["track_genre"] == "rock"].sample(n=1000, random_state=42),
    df[df["track_genre"] == "pop"].sample(n=1000, random_state=42),
    df[df["track_genre"] == "rap"].sample(n=1000, random_state=42),
    df[df["track_genre"] == "reggaeton"].sample(n=1000, random_state=42),
]).reset_index(drop=True)

print(df_balanced["track_genre"].value_counts())
print(f"\nTotal filas: {df_balanced.shape[0]}")


PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df_balanced.to_csv(PROCESSED_DIR / "spotify_clean.csv", index=False)
print("✅ Dataset limpio guardado en data/processed/spotify_clean.csv")