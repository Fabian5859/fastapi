# Proyecto individidual No. 1 - Sistema de recomendación de peliculas

Tabla de contenido
- [Introducción](#introducción)
- [Desarrollo del proyecto](#desarrollo-del-proyecto)
- [Retos del proyecto](#retos-del-proyecto)
- [Contacto](#contacto)

# Introducción
El objetivo de este proyecto es realizar un MVP del modelo de ML: un sistema de recomendación de pelìculas. 
En el proyecto del sistema de recomendación de películas se utiliza FastAPI para consumir los datos, y se realiza un deployment en render, para que los usuario puedan tener acceso a los siguietnes endpoint:
- Cantidad filmaciones mes: Retorna la cantidad de películas que fueron estrenadas en el mes consultado.
- Cantidad filmaciones día: Retorna la cantidad de películas que fueron estrenadas en el día consultado.
- score titulo: Retorna el score de una película consultada por título
- votos titulo:Retorna la cantidad y promedio de votos de una película consultada.
- Get Top 5 recomendaciones: Retorna la recomendación de las 5 peliculas más similares a la pelicula consultada. 

# Desarrollo del proyecto
Para el desarrollo del proyecto se utilizaron las siguientes herramientas:
- FastAPI
- Github
- Render

Se utilizaron las siguientes librerias de python:
- cosine_similarity. Para el sistema de recomendación de peliculas se utilizó la similitud del coseno.
- StandardScaler. Se realiza escalado de los datos, requerido para utilizar la similitud del coseno.
- Pandas. Para el preprocesamiento de los datos.
- matplotlib.pyplot y seaborn. Para el EDA del proyecto.

# Retos del proyecto
- El proyecto buscaba realizar un MVP (Mìnimo producto viable) cumpliendo un deadline, por lo cual era importante priorizar las tareas importantes.
- El dataset inicial requeria realizar un desanidado de los datos, ya que algunos campos tenian los datos como diccionarios o listas de diccionarios. Esta tarea demando un tiempo considerable en la ejecuciòn del proyecto, pero finalmente se logró resolver exitosamente.
- Para el desarrollo del proyectdo se debe investigar sobre las herramientas FastAPI y Render.
  

# Contacto
- Fabian Gutiérrez
- Correo eletrónico: programador5859@gmail.com
