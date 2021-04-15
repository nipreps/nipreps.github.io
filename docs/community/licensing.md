# Licensing and Derived Works

All software packages and tools under the *NiPreps* umbrella must be licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) by default, unless otherwise stated.
The authors of new *NiPreps* packages may not abide by this general rule of thumb if necessary and/or sufficiently justified (e.g., the source code is actually derived from a product licensed under a copyleft license).

Data (distributed within the test data of packages or through the [`nipreps-data` GitHub organization](https://github.com/nipreps-data)) will preferably be distributed under the [Creative Commons Zero v1.0 Universal](https://choosealicense.com/licenses/cc0-1.0/).

Under no circumstances any *NiPreps* software or data will be made publicly available unlicensed.
If you find any component of *NiPreps* that is unlicensed, please make us aware at nipreps@gmail.com at your earliest convenience.

## The Apache License 2.0

(This section is adapted from this [blog post by D. Marín](https://www.toptal.com/open-source/developers-guide-to-open-source-licenses))

The Apache License was created by the Apache Software Foundation (ASF) as the license for its Apache HTTP Server.

Just as the [MIT License](https://choosealicense.com/licenses/mit/), it’s a very permissive non-copyleft license that allows using the software for any purpose, distributing it, modifying it, and distributing derived works of it without concern for royalties. Its main differences, compared to the MIT License, are:

* Using the Apache License, the authors of the software grant patent licenses to any user or distributor of the code. This patent licenses apply to any patent that, being licenseable by any of the software author, would be infringed by the piece of code they have created.
* Apache License required that unmodified parts in derived works keep the License.
* In every licensed file, any original copyright, patent, trademark or attribution notices must be preserved.
* In every licensed file change, there must be a notification stating that changes have been made in the file.
* If the Apache-licensed software includes a `NOTICE` file, this file and its contents must be preserved in all the derived works.
* If anyone intentionally sends a contribution for an Apache-licensed software to its authors, this contribution can automatically be used under the Apache License.

This license is interesting because of the automatic patent license, and the clause about contribution submission.

It’s compatible with the GPL, so you can mix Apache licensed-code into GPL software.

## Why Apache-2.0?

In the case of scientific software, we believe that clearly stating that a Derived Work introduces changes into the original Work is a fundamental measure of transparency.
Other than that, we wanted a permissive, non-copyleft license.

## What is our expectation for Derived Works?

At the bare minimum, you must meet the conditions of the license ([simplified version](https://choosealicense.com/licenses/apache-2.0/)) about preserving the license text and copyright/attribution notices as well as corresponding statements of changes.

**How to state that a file has been changed in ad Derived Work.**
We suggest the following steps, heavily influenced by [P. Ombredanne's recommendations at StackExchange](https://opensource.stackexchange.com/a/4420):

1. In each source file, add a note to the header comment stating that the file has been modified, with an approximate date, and a high-level description of the changes.
   The date and the description of the changes are not strictly required, but they are positive etiquette from a software engineering standpoint and substantially improve the transparency of the changes from a scientific point of view.
1. If the source file did not have a license notice in the header comment, please add it to avoid ambiguity.
1. Deleted files: please keep the file with just the header comment and state that the file is deleted.
   The change statement should follow the suggestion in 1), preferably stating whether the source has been deleted or moved over to other files.
   If preserving the filename as-is might become confusing to the user of the Derived Work, the filename can be modified to be marked as hidden with a dot `.` or underscore `_` prefix, or modifying the extension.
1. Preferably, also include a link to the original file in our GitHub repository, making sure the link is done to a particular commit state.

**What changes would we like to see annotated?**
The *high-level description of the changes* will preferably contain:

* Correction of bugs
* Substantial performance improvement decisions
* Replacement of relevant methods and dependencies by alternatives
* Changes to the license

## Example of our expectations

Let's say a Derived Work modifies the `sdcflows.viz.utils` code-base.
Some files may not have the attribution notice.
At the time of writing, the header comment of [this file](https://github.com/nipreps/sdcflows/blob/50393a8584dd0abf5f8e16e6ba66c43e1126f844/sdcflows/viz/utils.py) is:

!!! example "Header comment in the original Work"

    === "With attribution notice"
	    ```{.python}
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
	    """Visualization tooling."""
	    ```
    === "Without attribution notice"
        ```{.python}
        # emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
        # vi: set ft=python sts=4 ts=4 sw=4 et:
        """Visualization tooling."""
        ```

Either way (whether the attribution notice is present or not), we suggest to update this header comment to something along the lines of the following:

!!! example "Suggested header comment in the Derived Work"

    ``` {.python hl_lines="5 6 19 20 21 22 23 24 25 26 27 28 29 30 31"}
    # <shebang and editor settings can be preserved or removed freely>
    #
    # <your attribution notice, either maintaining the Apache-2.0 license or changing the license>
    #
    # STATEMENT OF CHANGES: This file is derived from sources licensed under the Apache-2.0 terms,
    # and this file has been changed.
    # <recommended> The original file this work derives from is found at:
    # https://github.com/nipreps/sdcflows/blob/50393a8584dd0abf5f8e16e6ba66c43e1126f844/sdcflows/viz/utils.py
    # <alternative> The original file this work derives from is found within
    # the version 2.0.2 distribution of the software.
    #
    # <recommended> [April 2021] CHANGES:
    #    * BUGFIX: Outdated function call from the ``svgutils`` dependency that changed API as of version 0.3.2.
    #    * ENH: Changed plotting dependency to the new `netplotbrain` package.
    #    * DOC: Added docstrings to some functions that lacked them.
    #
    # ORIGINAL WORK'S ATTRIBUTION NOTICE:
    #
    #     Copyright 2021 The NiPreps Developers <nipreps@gmail.com>
    #     
    #     Licensed under the Apache License, Version 2.0 (the "License");
    #     you may not use this file except in compliance with the License.
    #     You may obtain a copy of the License at
    #     
    #         http://www.apache.org/licenses/LICENSE-2.0
    #     
    #     Unless required by applicable law or agreed to in writing, software
    #     distributed under the License is distributed on an "AS IS" BASIS,
    #     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    #     See the License for the specific language governing permissions and
    #     limitations under the License.
    """Visualization tooling."""
    ```

Only the lines highlighted are explicitly required by the Apache-2.0 conditions.
Although it is not mandated by the license letter, the spirit of the Apache-2.0 (and all other licenses stipulating the statement of changes, such as the CC-BY 4.0) suggests that a date of modification and an overview of outstanding changes are pertinent.
We also suggest a link to the original code, including the commit-hash (that long string starting with `50393a` in the URL above) for the location of the exact origin of the file.
Alternatively, Derived Works may point to a exact release identifier where the original file is part of the code-base distribution.
Please make sure to remove or replace with appropriate contents the comment tags `<...>` above.

**What if a Derived Work does not modify this particular file?**
You should retain the original attribution notice as is (or introduce it if missing), unless you are relicensing the file.
In that case, proceed with the suggestions above, and note the license change in the *STATEMENT OF CHANGES* block of the header comment.

## Are papers using Apache-2.0 licensed software considered as Derived Works?

No, they don't because they only ***reuse*** the software (in other words, they don't *redistribute* the software).
The license stipulates that *redistribution* must retain the license and attribution notices as they are.
In the scientific context, it is likely that a particular tool is modified (for example, to replace a method that you think is not appropriate for your data).
Then, *redistribution* of the source would be desirable from the transparent reporting point of view, and therefore you should honor the License.

Generally, works using our *NiPreps* just need to follow the citation guidelines of the particular project and report the *citation boilerplate* including all software versions and literature references in the closest letter possible to that generated by the tool.

## Licensing of Docker and Singularity images

Container images redistribute copies of *NiPreps* alongside their third-party dependencies, all of them bundled in the image.
That means that the text of a `NOTICE` file must be shown to the user.
All *NiPreps* must insert a `NOTICE` file into their containerized distributions and print its contents out in the command line output, as well as in the visual reports.
This `NOTICE` file for containers will be placed in the `/.docker/NOTICE` path of the repository.
If the particular project already has a `NOTICE` file, the contents of `/.docker/NOTICE` must be appended to the `/NOTICE` file at image building time.
