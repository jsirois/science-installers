# Copyright 2024 Science project contributors.
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import subprocess
import sys

from typing import Any


def main() -> Any:
    subprocess.run(["ruff", "format"], check=True)
    subprocess.run(["ruff", "check"], check=True)
    subprocess.run(["pytest", "-n", "auto"], check=True)


if __name__ == "__main__":
    sys.exit(main())
