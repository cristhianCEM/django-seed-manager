from random import randint, choice, uniform
from datetime import datetime, timedelta, timezone
from faker import Faker

DEFAULT_LOCALE = 'es_MX'
DEFAULT_TIMEZONE_OFFSET = -6
BOOLEANS = [True, False]


class SeedFaker:
    def __init__(self, locale=DEFAULT_LOCALE, timezone_hours_offset=DEFAULT_TIMEZONE_OFFSET):
        self.fake = Faker(locale)
        self.timezone_hours_offset = timezone_hours_offset
        self.timezone_delta = timedelta(hours=self.timezone_hours_offset)

    def boolean(self) -> bool:
        """Genera un valor booleano aleatorio."""
        return choice(BOOLEANS)

    def decision(self) -> bool:
        """Alias para generar un valor booleano aleatorio."""
        return self.boolean()

    def decimal(self, min_value: int = 0, max_value: int = 1, decimal_places: int = 2):
        """Genera un número decimal aleatorio dentro del rango especificado."""
        return round(uniform(min_value, max_value), decimal_places)

    def date_time_future(self, min_days=1, max_days=10):
        """Genera una fecha y hora futura en la zona horaria configurada."""
        today = datetime.now(tz=timezone(self.timezone_delta))
        return today + timedelta(days=randint(min_days, max_days))

    def date_between_years(self, min_year: int, max_year: int):
        """Genera una fecha aleatoria entre dos años dados."""
        if min_year > max_year:
            raise ValueError("El año mínimo no puede ser mayor que el año máximo.")
        return self.fake.date_between(start_date=f"{min_year}-01-01", end_date=f"{max_year}-12-31")

    def date_time_between_years(self, min_year: int, max_year: int):
        """Genera una fecha y hora aleatoria entre dos años dados."""
        if min_year > max_year:
            raise ValueError("El año mínimo no puede ser mayor que el año máximo.")
        return self.fake.date_time_between(start_date=f"{min_year}-01-01", end_date=f"{max_year}-12-31")

    def _apply_uppercase(self, text: str, uppercase: bool) -> str:
        """Aplica mayúsculas al texto si se indica."""
        return text.upper() if uppercase else text

    def name(self, uppercase: bool = False):
        """Genera un nombre aleatorio, con opción de convertirlo a mayúsculas."""
        return self._apply_uppercase(self.fake.name(), uppercase)

    def address(self, uppercase: bool = False):
        """Genera una dirección aleatoria, con opción de convertirla a mayúsculas."""
        return self._apply_uppercase(self.fake.address(), uppercase)

    def city(self, uppercase: bool = False):
        """Genera una ciudad aleatoria, con opción de convertirla a mayúsculas."""
        return self._apply_uppercase(self.fake.city(), uppercase)

    def text(self, max_nb_chars: int = 100, uppercase: bool = False):
        """Genera un texto aleatorio con una longitud máxima dada, con opción de convertirlo a mayúsculas."""
        fake_text = self.fake.text(max_nb_chars)
        return self._apply_uppercase(fake_text, uppercase)
