import chardet
from django.core.exceptions import ValidationError
from io import StringIO
from typing import List
import openpyxl
import csv
from typing import IO, List, Dict, Union
import json
from io import BytesIO, StringIO

# Tipos soportados de archivos

TYPE_JSON = 'json'
TYPE_CSV = 'csv'
TYPE_XLSX = 'xlsx'


class LoadFileJsonException(Exception):
    def __init__(self, message):
        self.message = "Error cargando el archivo JSON - " + message
        super().__init__(self.message)


class GetValuesFromExcelException(Exception):
    def __init__(self, exception: Exception):
        message = "Error al obtener la lista del archivo excel: "
        super().__init__(message + f"\n{exception}")


class GetRecordsFromCsvException(Exception):
    def __init__(self, exception: Exception):
        message = "Error al obtener la lista del archivo csv: "
        super().__init__(f"{message}\n{exception}")


def load_json_file(path: str, encoding: str = 'utf-8') -> Union[Dict, List]:
    """
    Carga datos JSON desde un archivo.
    Args:
        path (str): Ruta al archivo JSON.
        encoding (str): Codificación del archivo.
    Returns:
        Union[Dict, List]: Contenido del archivo JSON.
    """
    if not path or not path.endswith('.json'):
        raise LoadFileJsonException("La ruta está vacía o el archivo no es JSON.")
    try:
        with open(path, 'r', encoding=encoding) as file:
            return json.load(file)
    except FileNotFoundError:
        raise LoadFileJsonException(f"El archivo no se encontró en la ruta especificada: {path}")
    except json.JSONDecodeError as e:
        raise LoadFileJsonException(f"El archivo JSON tiene un formato inválido: {e}")


# init xslx functions


def get_values_from_excel(file: Union[IO, str]) -> List[List]:
    """
    Extrae valores de un archivo Excel, tal como esten en el archivo.
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
    records = []
    for row in values[1:]:
        row_data = {headers[i]: row[i] for i in range(len(headers))}
        records.append(row_data)
    return records

# init csv functions


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
    result = chardet.detect(raw_data)
    return result['encoding']


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


class UnsupportedImportFormat(Exception):
    def __init__(self, file_format: str):
        self.file_format = file_format
        super().__init__(f"El formato de archivo '{file_format}' no es soportado para la importación.")


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
        UnsupportedImportFormat(file_type)
