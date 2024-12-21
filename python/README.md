# inst-science

The `inst-science` Python project distribution provides two convenience console scripts to make
bootstrapping `science` for use in Python project easier:
+ `inst-science`: This is a shim script that ensures `science` is installed and forwards all
  supplied arguments to it. Instead of `science`, just use `inst-science`. You can configure the
  `science` version to use, where to find `science` binaries and where to install them via the 
  `[tool.inst-science]` table in your `pyproject.toml` file.
+ `inst-science-util`: This script provides utilities for managing `science` binaries. In
  particular, it supports downloading families of `science` binaries for various platforms for
  use in internal serving systems for offline or isolated installation.

## Development

Development uses [`uv`](https://docs.astral.sh/uv/getting-started/installation/). Install as you
best see fit.

With `uv` installed, running `uv run scripts/ci.py` is enough to get the tools inst-science uses
installed and run against the codebase. This includes formatting code, running lint checks and then
running tests.

