# Entrega 2 SD
### Paso 0: Ejecutar scrapping.py de manera independiente para obtener los .csv necesarios para las pruebas, estos deben estar en el formato "tiempo*", en donde '*' corresponde al numero de csv ascendente.
> tiempo1.csv, tiempo2.csv, tiempo3.csv, etc.
### Paso 1: Inicializar el dockerfile para preparar el entorno con el siguiente comando dentro de la carpeta Entrega2/
> docker-compose up --build
>
## En caso de que el dockerfile no funcione (y es bastante probable que no lo haga)
### Paso 1: Instalar requerimientos manualmente
> pip install -r requirements.txt
### Paso 2: Ejecutar script.sh en bash local. (Pull de la imagen y ejecucion del container.) Importante, el archivo podria requerir permisos de ejecucion.
> bash script.sh\
> chmod +x script.sh
## En caso de que script.sh no funcione.
### Paso 2.1.1 (En caso de que script.sh no funcione, se debe realizar el pull y la inicializacion manualmente.)
> docker pull fluddeni/hadoop-pig\
-- Inicializar la imagen\
> docker run -it   -v "$PWD:/scripts"   fluddeni/hadoop-pig   bash\
> -- con esto todo lo de Entrega2/ se incluira en el container del docker.
### Paso 2.1.2: Se deberia estar en el bash del contenedor, por lo que lo siguiente es
> cd scripts
### Paso 2.1.3: Ejecutar el archivo cargar_pig.py que llama al archivo .pig
>python cargar_pig.py
### Paso 2.1.4: Esto genera una carpeta resultados en el directorio local mediante el cual se tiene el archivo part-r-0000 que contiene los registros estandarizados.
