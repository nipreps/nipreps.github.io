# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2021 The NiPreps Developers <nipreps@gmail.com>
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
"""Query the GitHub API to retrieve the list of members."""

import os
import requests
from pathlib import Path


def main(argv=None):
    gh_token = os.getenv("GITHUB_TOKEN", None)

    if not gh_token:
        raise RuntimeError("No token")
    
    response = requests.get(
        "https://api.github.com/orgs/nipreps/members?per_page=100",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {gh_token}",
        }
    )
    
    if not response.ok:
        raise RuntimeError(f"Response failed ({response.code})")
    
    members = [
        f'<a href="{item["html_url"]}" target="_blank"><img class="avatar" src="{item["avatar_url"]}" /></a>'
        for item in response.json()
    ]

    target_file = Path(__file__).parent.parent / "docs" / "community" / "index.md"

    lines = target_file.read_text().splitlines()
    insert_line = len(lines)

    for line in reversed(lines):
        if line.strip().startswith("![[[members_grid]]]"):
            break
        insert_line -= 1

    lines = lines[:insert_line - 1] + members + lines[insert_line:]
    target_file.write_text(
        "\n".join(lines).replace("{{total_number_of_members}}", f"{len(members)}")
    )


if __name__ == "__main__":
    main()
