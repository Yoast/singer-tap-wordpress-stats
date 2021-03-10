# tap-wordpress-stats

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [WordPress.org Stats](hhttps://wordpress.org/about/stats/)
- Extracts the following resources:
  - WordPress versions
  - PHP versions
  - MySQL versions
  - Locales
- Outputs the schema for each resource
- Fully loads the statsistics on every run

---

Copyright &copy; 2021 Stitch
