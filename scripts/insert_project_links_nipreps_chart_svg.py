# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright The NiPreps Developers <nipreps@gmail.com>
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
"""Inserts links to the NiPreps project pages into the corresponding
elements of the NiPreps chart SVG file.

Example usage:

    python {script} input.svg project_links.json output.svg
    python {script} input.svg project_links.json --check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import urlopen

__doc__ = __doc__.format(script=Path(__file__).name)

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

NS = {"svg": SVG_NS, "xlink": XLINK_NS}
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)


def load_mapping(path: str) -> dict[str, str]:
    """Load label to URL mappings from a JSON file and validate string keys/values.

    Loads label to URL mappings from a JSON file and validates string keys/values.

    Parameters
    ----------
    path : :obj:`str`
        Path to a JSON file containing a top-level object of label→URL mappings.

    Returns
    -------
    :obj:`dict[str, str]`
        Normalized label-to-URL mapping.
    """

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Mapping file not found: {p}")

    text = p.read_text(encoding="utf-8")
    ext = p.suffix.lower()

    if ext == ".json":
        data = json.loads(text)
    else:
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            try:
                import yaml
            except ImportError as e:
                raise RuntimeError(
                    f"Unsupported mapping extension '{ext}'. Use .json."
                ) from e
            data = yaml.safe_load(text)

    if not isinstance(data, dict):
        raise ValueError("Mapping file must contain an object/dictionary at top level.")

    mapping: dict[str, str] = {}
    for k, v in data.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise ValueError("All mapping keys and values must be strings.")
        mapping[normalize(k)] = v.strip()

    return mapping


def normalize(s: str | None) -> str:
    """Normalize whitespaces in a label and trim leading/trailing spaces.

    Normalizes whitespaces in a label and trims leading/trailing spaces.

    Parameters
    ----------
    s : :obj:`str` | :obj:`None`
        Input text to normalize.

    Returns
    -------
    :obj:`str`
        Normalized text with collapsed internal whitespace.
    """
    return re.sub(r"\s+", " ", (s or "")).strip()


def localname(tag: str) -> str:
    """Return XML local tag name without namespace prefix.

    Returns XML local tag name without namespace prefix.

    Parameters
    ----------
    tag : :obj:`str`
        XML tag name, optionally namespace-qualified.

    Returns
    -------
    :obj:`str`
        Local (namespace-stripped) tag name.
    """
    return tag.split("}", 1)[-1] if "}" in tag else tag


def parse_svg(source: str) -> ET.ElementTree:
    """Parse an SVG from a local path or HTTP(S) URL into an ElementTree.

    Parses an SVG from a local path or HTTP(S) URL into an ElementTree.

    Parameters
    ----------
    source : :obj:`str`
        Local filesystem path or HTTP(S) URL to an SVG document.

    Returns
    -------
    :obj:`ET.ElementTree`
        Parsed SVG tree.
    """

    if source.startswith("http://") or source.startswith("https://"):
        with urlopen(source) as resp:
            data = resp.read()
        return ET.ElementTree(ET.fromstring(data))
    return ET.parse(source)


def find_parent(root: ET.Element, target: ET.Element) -> ET.Element | None:
    """Find and return the parent element of target within root, if present.

    Finds and returns the parent element of target within root, if present.

    Parameters
     ----------
    root : :obj:`ET.Element`
        Root element to search within.
    target : :obj:`ET.Element`
        Element whose direct parent should be found.

    Returns
    -------
    :obj:`ET.Element` | :obj:`None`
        Parent element if found, otherwise None.
    """
    for p in root.iter():
        for c in list(p):
            if c is target:
                return p
    return None


def already_linked(node: ET.Element, root: ET.Element) -> bool:
    """Return :obj:`True` if node is inside an existing SVG ``<a>`` element.

    Return :obj:`True` if node is inside an existing SVG ``<a>`` element.

    Parameters
    ----------
    node : :obj:`~ET.Element`
        Node to test for link ancestry.
    root : :obj:`~ET.Element`
        Root element used to traverse parent relationships.

    Returns
    -------
    :obj:`bool`
        :obj:`True` when any ancestor is an SVG anchor element;
        :obj:`False` otherwise.
    """
    cur = node
    while True:
        parent = find_parent(root, cur)
        if parent is None:
            return False
        if localname(parent.tag) == "a":
            return True
        cur = parent


def wrap_node_with_link(root: ET.Element, node: ET.Element, href: str) -> bool:
    """Wrap node in an SVG link (or update parent link href) and set target blank.

    Wraps the given node in an SVG link (or updates parent link href)
    and sets target blank.

    Parameters
    ----------
    root : :obj:`~ET.Element`
        Root element used to find parent relationships.
    node : :obj:`~ET.Element`
        Element to wrap in a link.
    href : :obj:`str`
        Destination URL for the SVG anchor.

    Returns
    -------
    :obj:`bool`
        :obj:`True` if the link was inserted or updated, :obj:`False`
        if wrapping was not possible.
    """

    parent = find_parent(root, node)
    if parent is None:
        return False

    if localname(parent.tag) == "a":
        parent.set(f"{{{XLINK_NS}}}href", href)
        parent.set("target", "_blank")
        return True

    children = list(parent)
    idx = children.index(node)
    parent.remove(node)

    a = ET.Element(f"{{{SVG_NS}}}a")
    a.set(f"{{{XLINK_NS}}}href", href)
    a.set("target", "_blank")
    a.append(node)

    parent.insert(idx, a)
    return True


def determine_best_click_target(root: ET.Element, text_node: ET.Element) -> ET.Element:
    """Prefer nearest <g> around text for click target; otherwise use text node.

    Prefer wrapping nearest ``<g>`` (icon plus text cluster) if
    available; fallback to ``<text>``.

    Parameters
    ----------
    root : :obj:`~ET.Element`
        Root element used to traverse parent relationships.
    text_node : :obj:`~ET.Element`
        Matched SVG text element.

    Returns
    -------
    :obj:`~ET.Element`
        The element that should be wrapped by an anchor.
   """
    cur = text_node
    while True:
        parent = find_parent(root, cur)
        if parent is None:
            return text_node
        if localname(parent.tag) == "g":
            # Stop at first group above text (usually project cluster)
            return parent
        cur = parent


def insert_links(tree: ET.ElementTree, mapping: dict[str, str]) -> int:
    """Insert links for mapped SVG text labels and return number of links inserted.

    Inserts links for mapped SVG text labels and return number of links
    inserted.

    Parameters
    ----------
    tree : :obj:`~ET.ElementTree`
        Parsed SVG tree to modify.
    mapping : :obj:`dict[str, str]`
        Label-to-URL mapping used to create links.

    Returns
    -------
    :obj:`int`
        Number of links inserted into the SVG.
    """

    root = tree.getroot()
    inserted = 0
    matched_labels = set()

    for text_node in root.findall(".//svg:text", NS):
        label = normalize("".join(text_node.itertext()))
        if label in mapping:
            matched_labels.add(label)
            target = determine_best_click_target(root, text_node)
            if not already_linked(target, root):
                if wrap_node_with_link(root, target, mapping[label]):
                    inserted += 1

    missing = sorted(set(mapping) - matched_labels)
    if missing:
        print(f"Warning: labels not found in SVG: {', '.join(missing)}")

    return inserted


def check_links(tree: ET.ElementTree, mapping: dict[str, str]) -> int:
    """Check SVG tree for missing elements or unlinked labels based on mapping

    Prints warnings for mapping labels that do not exist anywhere in the SVG,
    and returns a list of labels that exist in the SVG but currently lack a link.

    Parameters
    ----------
    tree : :obj:`~ET.ElementTree`
        Parsed SVG tree to check.
    mapping : :obj:`dict[str, str]`
        Label-to-URL mapping used to check links.

    Returns
    -------
    :obj:`int`
        Number of missing links that need to be inserted.
    """
    root = tree.getroot()
    unlinked_labels = []
    matched_labels = set()

    for text_node in root.findall(".//svg:text", NS):
        label = normalize("".join(text_node.itertext()))
        if label in mapping:
            matched_labels.add(label)
            target = determine_best_click_target(root, text_node)
            if not already_linked(target, root):
                unlinked_labels.append(label)

    # Print labels that do not exist in the SVG at all
    not_found = sorted(set(mapping) - matched_labels)
    if not_found:
        print(f"Warning: labels not found in SVG: {', '.join(not_found)}")

    return unlinked_labels


def _build_arg_parser() -> argparse.ArgumentParser:
    """Build argument parser for command-line interface.

    Returns
    -------
    :obj:`~argparse.ArgumentParser`
        Argument parser for the script.
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input", help="Input SVG file path or URL", type=Path)
    parser.add_argument("mapping",  help = "Path to mapping file (.json)", type=Path)
    parser.add_argument("output", help="Output SVG file path", type=Path, nargs="?")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if all project links are present without writing output (exits with 1 if missing)",
    )
    return parser


def _parse_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Parse command-line arguments.

    Parameters
    ----------
    parser : :obj:`~argparse.ArgumentParser`
        Argument parser for the script.

    Returns
    -------
    :obj:`~argparse.Namespace`
        Parsed arguments.
    """
    return parser.parse_args()


def main() -> None:
    parser = _build_arg_parser()
    args = _parse_args(parser)

    mapping = load_mapping(args.mapping)
    tree = parse_svg(str(args.input))

    if args.check:
        unlinked_labels = check_links(tree, mapping)
        unlinked_count = len(unlinked_labels)
        print(f"Check found {unlinked_count} projects missing link(s):")
        print(f"{unlinked_labels}")
        if unlinked_count > 0:
            sys.exit(1)
        else:
            print("All project links are present.")
            sys.exit(0)
    else:
        count = insert_links(tree, mapping)
        # Default to in-place editing if output wasn't provided
        out = Path(args.output if args.output else args.input)
        out.parent.mkdir(parents=True, exist_ok=True)
        tree.write(out, encoding="utf-8", xml_declaration=True)
        print(f"Inserted {count} link(s) into {out}")


if __name__ == "__main__":
    main()
