"""WordPress Stats tap."""
# -*- coding: utf-8 -*-
import logging
from argparse import Namespace

import pkg_resources
from singer import get_logger, utils
from singer.catalog import Catalog

from tap_wordpress_stats.discover import discover
from tap_wordpress_stats.sync import sync
from tap_wordpress_stats.wordpress_stats import WordPressStats

VERSION: str = pkg_resources.get_distribution('tap-wordpress-stats').version
LOGGER: logging.RootLogger = get_logger()


@utils.handle_top_exception(LOGGER)
def main() -> None:
    """Run tap."""
    # Parse command line arguments
    args: Namespace = utils.parse_args()

    LOGGER.info(f'>>> Running tap-wordpress-stats v{VERSION}')

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog: Catalog = discover()
        catalog.dump()
        return

    # Otherwise run in sync mode
    if args.catalog:
        # Load command line catalog
        catalog = args.catalog
    else:
        # Loadt the  catalog
        catalog = discover()

    # Initialize WordPress client
    wp: WordPressStats = WordPressStats()

    sync(wp, catalog)


if __name__ == '__main__':
    main()
