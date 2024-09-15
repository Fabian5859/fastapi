from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import List  # Importar List desde typing


df = pd.read_parquet("./Dataset/movies_dataset.parquet", engine='pyarrow')
df2 = pd.read_parquet("./Dataset/df_Recomendations.parquet", engine='pyarrow')

app = FastAPI()

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Función para obtener la cantidad de películas en un mes
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    mes = mes.lower()
    if mes in meses:
        mes_numero = meses[mes]
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        count = df[df['release_date'].dt.month == mes_numero].shape[0]
        return {"mensaje": f"{count} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}"}
    else:
        return {"mensaje": "Mes inválido"}

# Función para obtener la cantidad de películas en un día
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    dias = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
        'viernes': 4, 'sábado': 5, 'domingo': 6
    }
    dia = dia.lower()
    if dia in dias:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        count = df[df['release_date'].dt.dayofweek == dias[dia]].shape[0]
        return {"mensaje": f"{count} cantidad de películas fueron estrenadas en los días {dia.capitalize()}"}
    else:
        return {"mensaje": "Día inválido"}

# Función para obtener el score de una película por título
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    pelicula = df[df['title'].str.lower() == titulo.lower()]
    if not pelicula.empty:
        score = pelicula.iloc[0]['popularity']
        anio = pelicula.iloc[0]['release_year']
        return {"mensaje": f"La película {titulo} fue estrenada en el año {anio} con un score de {score}"}
    else:
        return {"mensaje": "Película no encontrada"}

# Función para obtener la cantidad y promedio de votos de una película
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    pelicula = df[df['title'].str.lower() == titulo.lower()]
    if not pelicula.empty:
        votos = pelicula.iloc[0]['vote_count']
        promedio = pelicula.iloc[0]['vote_average']
        if votos >= 2000:
            anio = pelicula.iloc[0]['release_year']
            return {"mensaje": f"La película {titulo} fue estrenada en el año {anio}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}"}
        else:
            return {"mensaje": "La película no cumple con la condición de 2000 valoraciones"}
    else:
        return {"mensaje": "Película no encontrada"}

# Función para obtener los datos de un actor
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    actor_peliculas = df[df['cast'].apply(lambda x: nombre_actor.lower() in str(x).lower())]
    if not actor_peliculas.empty:
        cantidad = actor_peliculas.shape[0]
        retorno_total = actor_peliculas['return'].sum()
        promedio_retorno = retorno_total / cantidad
        return {"mensaje": f"El actor {nombre_actor} ha participado de {cantidad} filmaciones, con un retorno total de {retorno_total} y un promedio de {promedio_retorno} por filmación"}
    else:
        return {"mensaje": "Actor no encontrado"}

# Función para obtener los datos de un director
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    director_peliculas = df[df['crew'].apply(lambda x: nombre_director.lower() in str(x).lower() and 'Director' in str(x))]
    if not director_peliculas.empty:
        detalles_peliculas = []
        for _, row in director_peliculas.iterrows():
            detalles_peliculas.append({
                "titulo": row['title'],
                "fecha_lanzamiento": row['release_date'],
                "retorno": row['return'],
                "costo": row['budget'],
                "ganancia": row['revenue']
            })
        retorno_total = director_peliculas['return'].sum()
        return {"mensaje": f"El director {nombre_director} ha tenido un retorno total de {retorno_total}. Detalles de sus películas:", "peliculas": detalles_peliculas}
    else:
        return {"mensaje": "Director no encontrado"}


@app.get('/get_recommendations/{base_movie_title}', response_model=List[str])
def get_top_5_recommendations(base_movie_title: str):
    try:
        # Verificar si la película base está en el DataFrame
        if base_movie_title not in df2['title'].values:
            raise HTTPException(status_code=404, detail=f"La película '{base_movie_title}' no se encuentra en el dataset.")
        
        # Paso 1: Preparar el Dataset
        features = ['vote_average', 'popularity', 'runtime', 'release_year']
        X = df2[features]

        # Normalizar las características
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Paso 2: Encontrar el índice de la película base
        movie_base_index = df2[df2['title'] == base_movie_title].index[0]
        movie_base_vector = X_scaled[movie_base_index].reshape(1, -1)

        # Paso 3: Calcular la Similitud del Coseno
        similarities = cosine_similarity(movie_base_vector, X_scaled).flatten()

        # Paso 4: Añadir la similitud al DataFrame
        df2['similarity'] = similarities

        # Paso 5: Obtener las 5 películas más similares
        recommendations = (df2[df2['title'] != base_movie_title]
                           .sort_values(by='similarity', ascending=False)
                           .head(5))
        
        # Devolver la lista de títulos
        top_5_titles = recommendations['title'].tolist()
        return top_5_titles

    except HTTPException as http_err:
        raise http_err  # Manejar errores HTTP específicos
    except Exception as e:
        # Manejo general de excepciones
        print(f"Error: {str(e)}")  # Puedes usar un logger en lugar de print en producción
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {str(e)}")
