
> The one bit that worries me is that *fMRIPrep* may become a Swiss army knife. I think instead it should just be a paring knife (small, efficient, and works for many things).
>
> -- <cite>Satra ([source](https://github.com/nipreps/fmriprep/issues/1963#issuecomment-584455061))</cite>

When projects grow large, many forking paths created by newly implemented features start
to open up.
To account for this, the *NiPreps* community was created with the vision of building
tools like *fMRIPrep* and *MRIQC* covering new imaging modalities, while keeping
existing *NiPreps* tightly within scope.
Defining such a scope also aids the implementation of the ease-of-use principle:

> The same way the scanner does not offer an immense space of knobs to turn
> in the acquisition, *NiPreps* should not add many additional knobs to those
> for them to be considered a viable *augmentation* or extension of the scanner hw/sw.
>
> -- <cite>Oscar ([source](https://github.com/nipreps/fmriprep/issues/1963#issuecomment-584455061))</cite>

## The problem of feature creep
To avert [feature creep](https://en.wikipedia.org/wiki/Feature_creep) and
to serve each individual *NiPrep*, we developed the following
guidelines, with the hopes of keeping these tools in a healthy state.

> I'm worried *fMRIPrep* is catching a case of featuritis
>
> -- <cite>Mathias ([source](https://github.com/nipreps/fmriprep/issues/1985#issuecomment-588493059))</cite>

These guidelines should also serve the community to transparently drive the process
of including proposals into the road-map, set the ground for healthy conversation,
and establish some patterns when accepting new-feature contributions.
Before proposing new features, please be mindful that a road-map may not exist
for a particular *NiPrep*.
Even when a development road-map exists, please understand that it is not always
possible to rigorously follow them:

> I think something like this is what we tried to start sketching out with
> the development roadmap. The concern, as I remember it, was that we couldn't
> guarantee (or rule out) specific features when working with a small
> development team.
>
> -- <cite>Elizabeth ([source](https://github.com/nipreps/fmriprep/issues/1963#issuecomment-582453941))</cite>.

## Proposing a new feature

### Why the new feature is requested?
Before going ahead and proposing a new feature, please take some time to
learn whether the topic has been covered in the past and what decisions
were made and why.
This should be reasonably easy to do with the search tool of GitHub on the
particular *NiPrep* repository.

If no previous discussion about the new idea is found,
the next step is ensuring the new feature aligns with the vision and
the scope of the target tool, as
[Elizabeth points out](https://github.com/nipreps/fmriprep/issues/1963#issuecomment-582453941).
Taking a look into the Development Road-map of the particular project
(if it exists), may help finding an answer.

If the new feature still seems pertinent after this preliminary work
or you are unsure about whether it falls within the scope, then
go ahead and post an issue requesting feedback on your proposal.
Please make sure to clearly state why the new feature should be considered.

### Some questions will always be asked about a new feature
[These questions by James](https://github.com/nipreps/fmriprep/issues/1963#issuecomment-582220173)
will certainly help build up the discourse in support of the new feature,
as the *NiPreps* maintainers will consider them:

  * **Is the user interface affected?**
    Because *NiPreps* generally expose a *command-line interface (CLI)* for the
    interaction with the user, new features involving changes to the CLI must be
    considered with caution as they may harm the ease-of-use:

    > It also seems that some new features add more confusion than others.
    > Especially when the CLI is affected, and yet another option is added,
    > that makes the tool more complex to use.
    >
    > -- <cite>Alejandro ([source](https://github.com/nipreps/fmriprep/    issues/1963#issuecomment-582174814))</cite>.

  * Does the new feature substantially **increase the internal complexity**?
    Maintainers and developers will attempt to consolidate tools and lower the internal
    complexity whenever possible.
    This effort usually competes with the addition of new features as they typically will
    address particular use-cases rather than general improvements.
    However, that doesn't need to be the case, as some sections of the code might be
    objectively improvable and the integration of a new feature revising those might
    also lower complexity.
    Lowering the internal complexity will always be considered a great incentive
    for a new feature to be accepted.

  * Is there **a standard procedure** for the proposed feature in the literature?

      * if so, could we just use that procedure/value?

  * Is the **feature dependent** on some attribute of the input data? (e.g., TR, duration, etc.)

      * if so, can the procedure/value be determined algorithmically?

  * Does the feature **interact with other settings**?
    For instance, [fmriprep#1962](https://github.com/nipreps/fmriprep/pull/1962)
    interacts with the a/tCompCor implementation.

  * What is the **difficulty of implementing the procedure outside** of a *NiPrep*?
    In other words, does the *NiPrep* provide all the necessary outputs for a
    user to perform the non-standard analysis?



### How the integration of the new feature will/can be validated?

Please propose ways to validate the new feature in the context of
the workflow. Meaning, the objective here is to validate that the new
feature works well within the pipeline, rather than validating a specific
algorithm.
To ensure the sustainability of *NiPreps*, the onus of this validation
should be on the person/group requesting the feature.
