
As of January 2020, *fMRIPrep* has adopted a [Calendar Versioning](https://calver.org) scheme, and with it we are attempting to apply more coherent semantic rules to our releases.

!!! warning "Note"
	This document is a draft for internal and external comment. Any commitments expressed here are proposals, and should not be relied upon at this time.
	This conversation started as a [Google Doc](https://docs.google.com/document/d/1hapyg61FRKZ2DqikVYKvckwQqnbobFQnnZoZi_WCDfo/edit?usp=sharing).

## Principles
The basic release form is `YY.MINOR.PATCH`, so the first minor release of 2020 is 20.0.0, and the first minor release of 2021 will be 21.0.0, whatever the final minor release of 2020 is. A series of releases share a `YY.MINOR.` prefix, which we refer to as the `YY.MINOR.x` series. For example, the 20.0.x series contains version 20.0.0, 20.0.1, and any other releases needed.

### Feature releases
Minor releases are considered *feature* releases. Because there is no concept of a "major" release (just a calendar year rollover), most changes to the code base will result in a new feature release. Changes targeting a new feature release should target the master branch. Feature releases may be released as often as is deemed appropriate.

### Bug-fix releases
Patch releases are considered bug-fix releases. Each minor release triggers the creation of a new `maint/<YY>.<MINOR>.x` branch, and changes targeting a bug-fix release should target this branch. A "minor release series" is the initial feature release and the bug-fix releases that share the minor release prefix. Bug-fix releases may be released on minimal notice to other developers.

These releases must satisfy four conditions:

1. **Resolving one or more bugs.** These mostly include failures of *fMRIPrep* to complete or producing invalid derivatives (e.g., a NIfTI file of all zeroes).
1. **Derivatives compatibility.** If a subject may be successfully run on 20.0.n, then the imaging derivatives should be identical if rerun with 20.0.(n+1), modulo rounding errors and the effects of nondeterministic algorithms. The changes between successful runs of 20.0.n and 20.0.(n+1) should not be larger than the changes between two successful runs of 20.0.n. Cosmetic changes to reports are acceptable, while differing fields of view or data types in a NIfTI file would not be.
1. **API compatibility.** Workflow-generating functions, workflow input- and outputnode fields must not change. As an end-user application, this may seem overly strict, but the odds of introducing a bug are much higher in these cases.
1. **User interface compatibility.** Substantial changes to *fMRIPrep* command line must not happen (e.g., the addition of a new, relevant flag).

Note that not all bugs can be fixed in a way that satisfies all four of these criteria without significant effort. A developer may determine that the bug will be fixed in the next feature release.

Additional acceptable changes within a minor release series:

1. **Improved tests.** These often come along with bug fixes, but they can be free-standing improvements to the code base.
1. **Improved documentation.** Unless the documentation is of a feature that will not be present in a bug-fix release, this is always welcome.
1. **Updates to the Dockerfile** that improve operation for Docker and/or Singularity users, but do not risk behavior change. A good example is including more templates to reduce the need for network requests. An example of an update to the Dockerfile that forces a minor release increment is a change in the pinned version of any of the dependencies or the base container image.
1. **Improvements to the *lightweight wrappers*.** As long as a command-line invocation that worked for the previous version continues to work and produce the same Docker command, there's little chance of harm.

## Mechanics

### Branch synchronization
A maintenance branch should generally follow directly from the tag of the feature release.
```
git checkout -b maint/20.0.x 20.0.0
git push upstream maint/20.0.x
```

It is expected that `maint/20.0.x` will diverge from `master`, as new features will be merged into `master`, and bug-fixes into `maint/20.0.x`. At a minimum, each new bug-fix release should be merged into `master`. After a `20.0.1` release:
```
git checkout master
git fetch upstream
git reset --hard upstream/master
git merge --no-commit 20.0.1

# Resolve any merge conflicts
git add .

# Manually review all changes to ensure compatibility
git diff --cached upstream/master
git commit
git push upstream master
```

If an unreleased bug-fix seems likely to cause merge conflicts, it may be worth doing the above more frequently.

### Dependencies
*fMRIPrep* has a number of dependencies that we control at this point:

1. sMRIPrep
1. SDCflows
1. NiWorkflows

These do not follow the same versioning scheme as above, but we need them to follow a compatible scheme. In particular, we need to be able to fix bugs that are situated within these dependencies in a bug-fix release without violating the criteria laid out above.
At the time of an *fMRIPrep* feature release, all of the above tools need to also split out a maintenance branch (if they have not already) for the minor version series that *fMRIPrep* depends on. As an example, when 20.0.0 was released, *fMRIPrep* had the following dependencies in [`setup.cfg`](https://github.com/nipreps/fmriprep/blob/20.0.0/setup.cfg#L22-L36):

```
    niworkflows ~= 1.1.7
    sdcflows ~= 1.2.0
    smriprep ~= 0.5.2
```
`~=` is the [compatible release specifier](https://www.python.org/dev/peps/pep-0440/#compatible-release) described in PEP 440. `~= 1.1.7` is equivalent to `>= 1.1.7, == 1.1.*`. This means that the current version of *fMRIPrep* is expected to work with niworkflows 1.1.7+ but not 1.2+.
Thus, niworkflows needs to have a maint/1.1.x branch, sdcflows a `maint/1.2.x` and smriprep `maint/0.5.x`. Any changes to these tools that might violate API or derivative compatibility, must go into master, and must not be released into the current minor series of these tools.
Note that *fMRIPrep* 20.0.0 does not depend on `niworkflows ~= 1.1.0`.
Multiple feature releases of *fMRIPrep* may depend on the same minor release series of a dependency. There is no requirement to hike the dependency. However, if a dependency has started a new minor release series, a feature release of *fMRIPrep* is a good opportunity to bump the dependency.

We maintain a [Versions Matrix](versions.md) to document and keep track of these dependencies.

## Support Windows
### Minor release series
A minor release series will continue to accept qualifying bug fixes **at least** until the next minor release. A minimum duration may be considered, or a fixed number of minor release series might be simultaneously supported.

An unmaintained series is a valid target for bug fixes after the support window, but the expected effort level of the contributor and maintainers will be higher and lower, respectively.

### Long-term support series
A long-term support (LTS) series is a minor release series that an LTS manager commits to maintaining for a specific duration, no less than one year. LTS series are under the same constraints as a minor release series in terms of what changes can be accepted.

The *fMRIPrep* developers commit to maintaining one LTS series at all times, at intervals of approximately one year. Community members may volunteer to assume maintainership after the initial period, or to maintain another minor release series as LTS.

Support windows of greater than a year have a much higher potential to run into issues with upstream dependencies going outside of their support windows. As much as possible, an *fMRIPrep* minor release should seek to move to the versions of upstream dependencies that will ensure the longest support before being considered for LTS.

Additional tasks required of an LTS manager:

* Tracking possible breaking changes and broken URLs in upstream projects outside of the nipreps ecosystem.
    * Neurodebian dependencies (AFNI, FSL, Convert3D, Connectome WB)
    * FreeSurfer
    * ANTs
    * NodeJS - BIDS-validator, SVGO
    * Pandoc
    * ICA-AROMA
    * Miniconda
    * Python minor series end-of-life
    * numpy, scipy, pandas, nipype, nibabel, matplotlib

* Backporting fixes from other maintained series.
    * If a bug is identified as existing within the LTS series and can be fixed without breaking API or derivative compatibility.

As many dependencies as possible should be pinned to specific versions relevant to the environment they are installed in. Packages (Debian `.deb` files, conda packages, Python wheels) should be archived in case of a loss of the external packages.
