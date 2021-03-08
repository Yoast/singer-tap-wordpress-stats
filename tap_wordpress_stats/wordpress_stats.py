"""WordPress.org stats fetcher."""
import logging
from datetime import datetime, timezone
from decimal import Decimal
from types import MappingProxyType
from typing import List

import httpx

API_SCHEME: str = 'https://'
API_BASE_URL: str = 'api.wordpress.org'
PATH_WORDPRESS: str = '/stats/wordpress/1.0/'
PATH_PHP: str = '/stats/php/1.0/'
PATH_MYSQL: str = '/stats/mysql/1.0/'
PATH_LOCALE: str = '/stats/locale/1.0/'

HEADERS: MappingProxyType = MappingProxyType({
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/74.0.3729.131 Safari/537.36'
    ),
})


class WordPressStats(object):
    """WordPress Stats."""

    @classmethod
    def load(cls, url: str) -> dict:
        """Load an URL and return JSON.

        Arguments:
            url {str} -- URL to fetch from

        Returns:
            dict -- JSON as dict
        """
        logging.info(f'Loading: {url}')
        client: httpx.Client = httpx.Client(http2=False)
        response: httpx._models.Response = client.get(  # noqa: WPS437
            url,
            headers=dict(HEADERS),
        )

        return response.json()

    @classmethod
    def wordpress(cls) -> List[dict]:
        """Wordpress stats.

        Returns:
            List[dict] -- List of WordPress versions
        """
        wp_data: dict = cls.load(f'{API_SCHEME}{API_BASE_URL}{PATH_WORDPRESS}')
        return cls._transform_version(wp_data)

    @classmethod
    def php(cls) -> List[dict]:
        """Php stats.

        Returns:
            List[dict] -- List of PHP versions
        """
        wp_data: dict = cls.load(f'{API_SCHEME}{API_BASE_URL}{PATH_PHP}')
        return cls._transform_version(wp_data)

    @classmethod
    def mysql(cls) -> List[dict]:
        """Mysql stats.

        Returns:
            List[dict] -- List of MySQL versions
        """
        wp_data: dict = cls.load(f'{API_SCHEME}{API_BASE_URL}{PATH_MYSQL}')
        return cls._transform_version(wp_data)

    @classmethod
    def locale(cls) -> List[dict]:
        """Locale stats.

        Returns:
            List[dict] -- List of locales
        """
        wp_data: dict = cls.load(f'{API_SCHEME}{API_BASE_URL}{PATH_LOCALE}')

        now: str = datetime.now(tz=timezone.utc).replace(
            microsecond=0,
        ).isoformat()

        return [
            {
                'timestamp': now,
                'locale': locale,
                'percentage': Decimal(str(percentage)) / 100,
            } for locale, percentage in wp_data.items()
        ]

    @classmethod
    def _transform_version(cls, wp_data: dict) -> List[dict]:
        """Transform a dictionary of versions to a list of versions.

        Arguments:
            wp_data {dict} -- WordPress data

        Returns:
            List[dict] -- List of WordPress data
        """
        now: str = datetime.now(tz=timezone.utc).replace(
            microsecond=0,
        ).isoformat()

        return [
            {
                'timestamp': now,
                'version': version,
                'percentage': Decimal(str(percentage)) / 100,
            } for version, percentage in wp_data.items()
        ]
