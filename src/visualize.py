import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
# Cargar DataSet
BASE_DIR = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE_DIR / "data" / "processed" / "spotify_clean.csv")

# Crear una figura con plt.subplots de 2 filas y 2 columnas ( una por genero)
fig, ax = plt.subplots(2, 2, figsize=(10, 10))

# Para cada genero, filtra el DataFrame y dibuja un histograma de tempo con sns.histplot
# Añadir titulo, etiquetas y exporta con plt.savefig
for i, genre in enumerate(df["track_genre"].unique()):
    df_genre = df[df["track_genre"] == genre]
    sns.histplot(x="tempo", data=df_genre, ax=ax[i // 2, i % 2])
    ax[i // 2, i % 2].set_title(genre)
    ax[i // 2, i % 2].set_xlabel("Tempo (BPM)")
    ax[i // 2, i % 2].set_ylabel("Frecuencia")
plt.savefig(BASE_DIR / "visualizations" / "tempo_by_genre.png")

# Crea una figura simple con plt.subplots
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Usa sns.scatterplot con x="energy" , y="danceability", hue="track_genre", hue coloreará cada genero automaticamente.
# Añadir titulo, etiquetas y exporta a visualizations/energy_vs_danceability.png
sns.scatterplot(x="energy", y="danceability", hue="track_genre", data=df, ax=ax)
ax.set_title("Energía vs. Danceability")
ax.set_xlabel("Energía")
ax.set_ylabel("Danceability")
plt.savefig(BASE_DIR / "visualizations" / "energy_vs_danceability.png")

# Selecciona solo las columnas numéricas relevantes: popularity, danceability, energy, valence, tempo, duration_ms
df_correlation = df[["popularity", "danceability", "energy", "valence", "tempo", "duration_ms"]]
# Calcula la matriz de correlación con .corr()
correlation_matrix = df_correlation.corr()
plt.figure(figsize=(8,6))
# Usa sns.heatmap con annot=True para mostrar los valores dentro de cada celda
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Matriz de Correlación")
# Exportar a visualizations/correlation_heatmap.png
plt.savefig(BASE_DIR / "visualizations" / "correlation_heatmap.png", dpi=150, bbox_inches="tight")

# Crea una figura con plt.figure
# Usa sns.boxplot con x="track_genre", y="popularity", hue="track_genre" y data=df
plt.figure(figsize=(10,6))
sns.boxplot(x="track_genre", y="popularity", hue="track_genre", data=df)
# Añadir titulo, etiquetas
ax.set_title("Distribución de Popularidad por Genero")
ax.set_xlabel("Genero")
ax.set_ylabel("Popularidad")
plt.savefig(BASE_DIR / "visualizations" / "popularity_by_genre.png")



plt.show()

