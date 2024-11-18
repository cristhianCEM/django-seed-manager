from abc import ABC, abstractmethod
from typing import List, Dict


class FileHandler(ABC):
    """
    Contrato base para todos los manejadores de archivos.
    """
    @abstractmethod
    def load(self, file):
        """Carga el archivo para su procesamiento."""
        pass

    @abstractmethod
    def get_records(self) -> List[Dict]:
        """Devuelve los registros del archivo como una lista de diccionarios."""
        pass


class UnsupportedImportFileFormat(Exception):
    """Excepción para formatos de archivo no soportados."""

    def __init__(self, file_format: str):
        super().__init__(f"El formato de archivo '{file_format}' no es soportado para la importación.")


class FileHandlerRegistry:
    """
    Registro de manejadores de archivos.
    """

    def __init__(self):
        self.handlers = {}

    def register_handler(self, file_format: str, handler: FileHandler):
        """Registra un nuevo manejador para un tipo de archivo."""
        self.handlers[file_format] = handler

    def get_handler(self, file_format: str) -> FileHandler:
        """Obtiene el manejador para un tipo de archivo."""
        if file_format not in self.handlers:
            raise UnsupportedImportFileFormat(file_format)
        return self.handlers[file_format]
