# insta-science

The `insta-science` Python project distribution provides two convenience console scripts to make
bootstrapping `science` for use in Python project easier:
+ `insta-science`: This is a shim script that ensures `science` is installed and forwards all
  supplied arguments to it. Instead of `science`, just use `insta-science`. You can configure the
  `science` version to use, where to find `science` binaries and where to install them via the 
  `[tool.insta-science]` table in your `pyproject.toml` file.
+ `insta-science-util`: This script provides utilities for managing `science` binaries. In
  particular, it supports downloading families of `science` binaries for various platforms for
  use in internal serving systems for offline or isolated installation.

This project is under active early development and APIs and configuration are likely to change
rapidly in breaking ways until the 1.0 release.

## Development

Development uses [`uv`](https://docs.astral.sh/uv/getting-started/installation/). Install as you
best see fit.

With `uv` installed, running `uv run dev-cmd` is enough to get the tools insta-science uses installed
and run against the codebase. This includes formatting code, linting code, performing type checks
and then running tests.
