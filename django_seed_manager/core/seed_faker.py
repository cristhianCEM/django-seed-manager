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
        return choice(BOOLEANS)

    def decision(self) -> bool:
        return choice(BOOLEANS)

    def decimal(self, min_value: int = 0, max_value: int = 1, decimal_places: int = 2):
        return round(uniform(min_value, max_value), decimal_places)

    def date_time_future(self, min_days=1, max_days=10):
        today = datetime.now(timezone.utc) + self.timezone_delta
        return today + timedelta(days=randint(min_days, max_days))

    def date_between_years(self, min_year: int, max_year: int):
        return self.fake.date_between(start_date=f"{min_year}-01-01", end_date=f"{max_year}-12-31")

    def date_time_between_years(self, min_year: int, max_year: int):
        return self.fake.date_time_between(start_date=f"{min_year}-01-01", end_date=f"{max_year}-12-31")

    def name(self, uppercase: bool = False):
        result = self.fake.name()
        return result.upper() if uppercase else result

    def address(self, uppercase: bool = False):
        result = self.fake.address()
        return result.upper() if uppercase else result

    def city(self, uppercase: bool = False):
        result = self.fake.city()
        return result.upper() if uppercase else result

    def text(self, max_nb_chars: int = 100, uppercase: bool = False):
        result = self.fake.text(max_nb_chars)
        return result.upper() if uppercase else result
