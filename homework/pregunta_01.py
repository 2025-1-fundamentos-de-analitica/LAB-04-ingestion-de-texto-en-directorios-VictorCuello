# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```
    """
    import zipfile
    import os
    import pandas as pd

    # Paso 1: Descomprimir el archivo ZIP.
    # El archivo 'files/input.zip' se descomprimirá en el directorio raíz,
    # creando la carpeta 'input/'.
    if os.path.exists("input"):
        import shutil
        shutil.rmtree("input")
        
    with zipfile.ZipFile("files/input.zip", "r") as zip_ref:
        zip_ref.extractall()

    # --- INICIO DE LA CORRECCIÓN ---
    # La prueba espera que la carpeta de salida esté en 'files/output/'.
    # Se define la ruta de salida correctamente.
    output_dir = "files/output"
    # --- FIN DE LA CORRECCIÓN ---

    # Paso 2: Asegurarse de que el directorio de salida exista.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    def process_directory(dataset_path):
        """
        Lee todos los archivos de texto de una ruta de conjunto de datos (ej. 'input/train')
        y extrae la frase y el sentimiento (basado en el subdirectorio).
        Retorna una lista de tuplas (frase, sentimiento).
        """
        data = []
        sentiments = ["positive", "negative", "neutral"]

        for sentiment in sentiments:
            sentiment_path = os.path.join(dataset_path, sentiment)
            if not os.path.isdir(sentiment_path):
                continue
            
            # Ordenar los archivos para un procesamiento determinista y consistente
            filenames = sorted(os.listdir(sentiment_path))
            for filename in filenames:
                if filename.endswith(".txt"):
                    file_path = os.path.join(sentiment_path, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        # Leer contenido, limpiar espacios y saltos de línea
                        phrase = f.read().strip().replace("\n", " ")
                        data.append((phrase, sentiment))
        return data

    # Paso 3: Procesar los datos de entrenamiento y prueba.
    # Las rutas de entrada son relativas a la raíz del proyecto.
    train_data = process_directory("input/train")
    test_data = process_directory("input/test")

    # Paso 4: Crear DataFrames de pandas.
    # Se usa el nombre de columna 'target' según el ejemplo en la descripción.
    train_df = pd.DataFrame(train_data, columns=["phrase", "target"])
    test_df = pd.DataFrame(test_data, columns=["phrase", "target"])

    # Paso 5: Guardar los DataFrames en archivos CSV en la carpeta 'output' corregida.
    # Se omite el índice del DataFrame en el archivo CSV.
    train_df.to_csv(os.path.join(output_dir, "train_dataset.csv"), index=False)
    test_df.to_csv(os.path.join(output_dir, "test_dataset.csv"), index=False)
    
    # Limpieza de la carpeta descomprimida para no interferir con otras ejecuciones.
    import shutil
    shutil.rmtree("input")