import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Cargar el dataset con la ruta dinamica
BASE_DIR = Path(__file__).resolve().parent.parent
VIZ_DIR = BASE_DIR / "visualizations"

df = pd.read_csv(BASE_DIR / "data" / "processed" / "spotify_clean.csv")
print(df.head())

# Seleccionar las columnas "danceability", "energy", "valence", "tempo"
# Crear un StandardScaler() y aplicarlo con .fit_transform(), guardar el resultado en una variable X_scaled
X_scaled = StandardScaler().fit_transform(df[["danceability", "energy", "valence", "tempo"]])

# Crear una lista vacia
inertias = []

# Bucle for 
for k in range(1, 11):
    # crear un KMeans(n_clusters=k) y entrenarlo con X_scaled y añadir la inertia_ a la lista
    kmeans = KMeans(n_clusters=k).fit(X_scaled)
    inertias.append(kmeans.inertia_)
# Graficar inertas con plt.plot
plt.plot(range(1, 11), inertias, marker="o") # marker es para ver los puntos
plt.xticks(range(1, 11)) # muestra los numeros en el eje x
plt.xlabel("Numero de Clusters")
plt.ylabel("Inertia")
plt.title("Inertia vs Número de Clusters")
plt.savefig(VIZ_DIR / "elbow_method.png")

# Crear un Kmeans(n_clusters=4, random_state=42) y entrenarlo con X_scaled
# Añadir los clusters al DataFrame con df["cluster"] = kmeans.labels_
#Imprimir df["cluster"].value_counts() para ver cuantas canciones hay en cada cluster
kmeans = KMeans(n_clusters=4, random_state=42).fit(X_scaled)
df["cluster"] = kmeans.labels_
print(df["cluster"].value_counts())
print(pd.crosstab(df["track_genre"], df["cluster"]))

# Crea un PCA(n_components=2) y aplicalo con .fit_transform(), sobre X_scaled
# guardar el resultado en una variable X_pca
# Crear un DataFrame con las dos componentes y el cluster: columnas PC1, PC2y cluster
# Usa sns.scatterplot con x="PC1", y="PC2", hue="cluster"
# exportar a visualizations/kmeans_clusters.png
X_pca = PCA(n_components=2).fit_transform(X_scaled)
df_pca = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
df_pca["cluster"] = df["cluster"].values
# Usar plt.figure
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_pca, x="PC1", y="PC2", hue="cluster", palette="tab10", alpha=0.6)
# Añadir titulo, etiquetas
ax = plt.gca()
ax.set_title("Clusters de Kmeans")
ax.set_xlabel("Componente 1")
ax.set_ylabel("Componente 2")
plt.savefig(VIZ_DIR / "kmeans_clusters.png")
plt.show()
