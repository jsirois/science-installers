# Copyright 2024 Science project contributors.
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import timedelta
from pathlib import Path, PurePath
from subprocess import CalledProcessError
from typing import NoReturn

import colors
import httpx
from packaging.version import Version

from insta_science import a_scie, parser, project
from insta_science.cache import Missing, download_cache
from insta_science.errors import InputError
from insta_science.hashing import ExpectedDigest
from insta_science.model import Science
from insta_science.platform import Platform


def _find_science_on_path(science: Science) -> PurePath | None:
    cache = download_cache()
    url = f"file://{cache.base_dir}/science"
    ttl: timedelta | None = None
    if science.version:
        url = f"{url}/v{science.version}"
        if science.digest:
            url = f"{url}#{science.digest.fingerprint}:{science.digest.size}"
    else:
        ttl = timedelta(days=5)

    with cache.get_or_create(url=url, ttl=ttl) as cache_result:
        if isinstance(cache_result, Missing):
            current_platform = Platform.current()
            for binary_name in (
                current_platform.binary_name("science"),
                current_platform.binary_name("science-fat"),
                current_platform.qualified_binary_name("science"),
                current_platform.qualified_binary_name("science-fat"),
            ):
                science_exe = shutil.which(binary_name)
                if not science_exe:
                    continue
                if science.version:
                    if science.version != Version(
                        subprocess.run(
                            args=[science_exe, "-V"], text=True, stdout=subprocess.PIPE
                        ).stdout.strip()
                    ):
                        continue
                    if science.digest and science.digest.fingerprint:
                        expected_digest = ExpectedDigest(
                            fingerprint=science.digest.fingerprint, size=science.digest.size
                        )
                        try:
                            expected_digest.check_path(Path(science_exe))
                        except InputError:
                            continue
                shutil.copy(science_exe, cache_result.work)
                return cache_result.path
            return None
    return cache_result.path


def science(spec: Science | None = None) -> NoReturn:
    """Ensures an appropriate science binary is installed and then forwards to it.

    spec: An optional specification of which science binary is required.
    """
    if spec is not None:
        science = spec
    else:
        try:
            pyproject_toml = project.find_pyproject_toml()
            science = parser.configured_science(pyproject_toml) if pyproject_toml else Science()
        except InputError as e:
            sys.exit(f"{colors.red('Configuration error')}: {colors.yellow(str(e))}")

    try:
        science_exe = _find_science_on_path(science) or a_scie.science(science)
    except (
        OSError,
        CalledProcessError,
        InputError,
        httpx.HTTPError,
        httpx.InvalidURL,
        httpx.CookieConflict,
        httpx.StreamError,
    ) as e:
        sys.exit(colors.red(str(e)))

    argv = [str(science_exe), *sys.argv[1:]]
    try:
        if Platform.current() in (Platform.Windows_aarch64, Platform.Windows_x86_64):
            sys.exit(subprocess.run(argv).returncode)
        else:
            os.execv(science_exe, argv)
    except OSError as e:
        sys.exit(colors.red(str(e)))
