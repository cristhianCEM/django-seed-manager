import chardet
from django.core.exceptions import ValidationError
from io import StringIO, BytesIO
from typing import List, IO, Dict, Union
import openpyxl
import csv
import json
import os

TYPE_JSON = 'json'
TYPE_CSV = 'csv'
TYPE_XLSX = 'xlsx'


# Excepciones
class LoadFileJsonException(Exception):
    """Excepción para errores al cargar archivos JSON."""
    def __init__(self, message: str):
        super().__init__(f"Error cargando el archivo JSON - {message}")


class GetValuesFromExcelException(Exception):
    """Excepción para errores al procesar un archivo Excel."""
    def __init__(self, exception: Exception):
        super().__init__(f"Error al obtener la lista del archivo Excel: {exception}")


class GetRecordsFromCsvException(Exception):
    """Excepción para errores al procesar un archivo CSV."""
    def __init__(self, exception: Exception):
        super().__init__(f"Error al procesar el archivo CSV: {exception}")


class UnsupportedImportFormat(Exception):
    """Excepción para formatos de archivo no soportados."""
    def __init__(self, file_format: str):
        super().__init__(f"El formato de archivo '{file_format}' no es soportado para la importación.")


# Funciones de Validación
def is_valid_extension(path: str, valid_extensions: List[str]) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in valid_extensions


# Funciones de carga
def load_json_file(path: Union[str, IO], encoding: str = 'utf-8') -> Union[Dict, List]:
    """
    Carga datos JSON desde un archivo.
    Args:
        path (str o IO): Ruta al archivo JSON o archivo en BytesIO.
        encoding (str): Codificación del archivo.
    Returns:
        Union[Dict, List]: Contenido del archivo JSON.
    """
    if isinstance(path, str) and not path.endswith('.json'):
        raise LoadFileJsonException("La ruta no apunta a un archivo JSON válido.")
    try:
        if isinstance(path, str):
            with open(path, 'r', encoding=encoding) as file:
                return json.load(file)
        else:
            return json.load(path)
    except Exception as e:
        raise LoadFileJsonException(str(e))


def get_values_from_excel(file: Union[IO, str]) -> List[List]:
    """
    Extrae valores de un archivo Excel.
    Args:
        file (IO o str): Archivo Excel o ruta al archivo.
    Returns:
        List[List]: Valores del archivo Excel como lista de listas.
    """
    try:
        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        return [list(row) for row in sheet.iter_rows(values_only=True)]
    except Exception as e:
        raise GetValuesFromExcelException(e)


def get_records_from_excel(file: Union[IO, str]) -> List[Dict]:
    """
    Convierte un archivo Excel en una lista de diccionarios.
    Args:
        file (IO o str): Archivo Excel o ruta al archivo.
    Returns:
        List[Dict]: Registros del archivo como lista de diccionarios.
    """
    values = get_values_from_excel(file)
    if not values:
        return []
    headers = values[0]
    return [
        {headers[i]: row[i] for i in range(len(headers))}
        for row in values[1:]
    ]


def detect_encoding(file: BytesIO) -> str:
    """
    Detecta la codificación de un archivo.
    Args:
        file (BytesIO): Archivo en formato de bytes.
    Returns:
        str: Codificación detectada.
    """
    raw_data = file.read(10000)
    file.seek(0)
    return chardet.detect(raw_data)['encoding']


def get_stringio_from_file(file: BytesIO) -> StringIO:
    """
    Convierte un archivo en BytesIO a StringIO con codificación detectada.
    Args:
        file (BytesIO): Archivo en formato de bytes.
    Returns:
        StringIO: Archivo en formato de texto.
    """
    encoding = detect_encoding(file)
    file_data = file.read().decode(encoding)
    file.seek(0)
    return StringIO(file_data)


def get_records_from_csv(file: Union[BytesIO, StringIO]) -> List[Dict]:
    """
    Convierte un archivo CSV en una lista de diccionarios.
    Args:
        file (BytesIO o StringIO): Archivo CSV o stream.
    Returns:
        List[Dict]: Registros del archivo como lista de diccionarios.
    """
    try:
        if isinstance(file, BytesIO):
            file = get_stringio_from_file(file)
        reader = csv.DictReader(file)
        return [row for row in reader]
    except Exception as e:
        raise GetRecordsFromCsvException(e)


def load_file(file: Union[IO, str], file_type: str) -> List[Dict]:
    """
    Carga un archivo en formato JSON, CSV o Excel según el tipo especificado.
    Args:
        file (IO o str): Archivo o ruta al archivo.
        file_type (str): Tipo de archivo ('json', 'csv', 'xlsx').
    Returns:
        List[Dict]: Contenido del archivo.
    """
    if not file:
        raise ValidationError("No se ha proporcionado un archivo.")

    if file_type == TYPE_JSON:
        return load_json_file(file)
    elif file_type == TYPE_CSV:
        return get_records_from_csv(file)
    elif file_type == TYPE_XLSX:
        return get_records_from_excel(file)
    else:
        raise UnsupportedImportFormat(file_type)
