import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ruta de los archivos CSV
results_path = 'results/'

# Lista para guardar los resultados
summary = []

# Contador de ejecuciones
ejecucion_num = 1

# Procesar cada archivo CSV
for file in sorted(os.listdir(results_path)):
    if file.endswith('.csv'):
        file_path = os.path.join(results_path, file)

        try:
            # Leer el archivo con codificación robusta
            df = pd.read_csv(file_path, encoding='latin1')

            if 'Fitness' in df.columns:
                min_fitness = df['Fitness'].min()
                gen_min = df['Fitness'].idxmin() + 1  # índice humano
                summary.append({
                    'Ejecución': f'Ejecución {ejecucion_num}',
                    'Mejor Fitness': min_fitness,
                    'Generación': gen_min
                })
                ejecucion_num += 1
        except Exception as e:
            print(f"Error al leer {file}: {e}")

# Crear DataFrame resumen
summary_df = pd.DataFrame(summary)
summary_df = summary_df.sort_values(by='Mejor Fitness').reset_index(drop=True)

# Mostrar tabla en consola
print(summary_df)

# Guardar resumen en CSV
summary_df.to_csv('mejores_fitness.csv', index=False)
print("\nResumen guardado en 'mejores_fitness.csv'")

# Gráfica
plt.figure(figsize=(10, 6))
plt.barh(summary_df['Ejecución'], summary_df['Mejor Fitness'], color='steelblue')
plt.xlabel('Mejor Fitness')
plt.title('Comparación de mejores fitness por ejecución')
plt.tight_layout()
plt.show()


df = pd.read_csv('mejores_fitness.csv')

# Estadísticas generales
print("=== Estadísticas de Fitness ===")
print(df['Mejor Fitness'].describe())
print("\n=== Estadísticas de Generación del mejor fitness ===")
print(df['Generación'].describe())

# Histograma del Mejor Fitness
plt.figure(figsize=(8, 5))
sns.histplot(df['Mejor Fitness'], bins=10, kde=True, color='teal')
plt.title('Distribución de mejores Fitness')
plt.xlabel('Mejor Fitness')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.show()

# Histograma de la generación del mejor fitness
plt.figure(figsize=(8, 5))
sns.histplot(df['Generación'], bins=10, kde=True, color='coral')
plt.title('Distribución de generación del mejor fitness')
plt.xlabel('Generación')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.show()

# Boxplot del Mejor Fitness
plt.figure(figsize=(6, 4))
sns.boxplot(x=df['Mejor Fitness'], color='lightgreen')
plt.title('Boxplot del Mejor Fitness')
plt.tight_layout()
plt.show()

# Dispersión: Mejor Fitness vs. Generación
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Generación', y='Mejor Fitness', hue='Ejecución', palette='tab10')
plt.title('Relación entre Generación y Mejor Fitness')
plt.xlabel('Generación donde se obtuvo')
plt.ylabel('Mejor Fitness')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()