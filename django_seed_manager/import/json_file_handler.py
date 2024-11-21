import json
from .file_handler import FileHandler
from typing import List, Dict, Union, IO

DEFAULT_ENCODING = 'utf-8'


class LoadFileJsonException(Exception):
    """Excepción para errores al cargar archivos JSON."""

    def __init__(self, message: str):
        super().__init__(f"Error cargando el archivo JSON - {message}")


class JSONFileHandler(FileHandler):
    """
    Manejador para archivos JSON.
    """

    allow_multiple_models = True

    def load(self, file_path: Union[str, IO], encoding: str = DEFAULT_ENCODING) -> Union[Dict, List]:
        """
        Carga datos JSON desde un archivo.
        Args:
            file_path (str o IO): Ruta al archivo o IO stream.
            encoding (str): Codificación del archivo.
        Returns:
            Union[Dict, List]: Contenido del archivo JSON.
        """
        if isinstance(file_path, str) and not file_path.endswith('.json'):
            raise LoadFileJsonException("La ruta no apunta a un archivo JSON válido.")
        try:
            if isinstance(file_path, str):
                with open(file_path, 'r', encoding=encoding) as file:
                    return json.load(file)
            else:
                return json.load(file_path)
        except Exception as e:
            raise LoadFileJsonException(str(e))
