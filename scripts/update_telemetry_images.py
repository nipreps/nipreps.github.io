# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2024 The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""Update references to telemetry charts on the landing page."""

import re
from pathlib import Path


ASSETS_DIR = Path(__file__).parent.parent / "docs" / "assets"
INDEX_FILE = Path(__file__).parent.parent / "docs" / "index.md"

WEEKLY_RE = re.compile(r"assets/\d{8}_weekly.png")
VERSIONSTREAM_RE = re.compile(r"assets/\d{8}_versionstream.png")


def _latest(pattern: str) -> str | None:
    files = sorted(ASSETS_DIR.glob(pattern))
    return files[-1].name if files else None


def main(argv=None):  # noqa: D401
    """Update the links in the index page to the newest telemetry charts."""
    weekly_file = _latest("*_weekly.png")
    version_file = _latest("*_versionstream.png")

    if not weekly_file or not version_file:
        return

    text = INDEX_FILE.read_text()
    text = WEEKLY_RE.sub(f"assets/{weekly_file}", text)
    text = VERSIONSTREAM_RE.sub(f"assets/{version_file}", text)
    INDEX_FILE.write_text(text)


if __name__ == "__main__":
    main()
