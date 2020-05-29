# Framework

## Building on *fMRIPrep*'s success story

The current neuroimaging workflow has matured into a large chain of processing and analysis steps involving a large number of experts, across imaging modalities and applications.
The development and fast adoption of [*fMRIPrep*][1] have revealed that neuroscientists need tools that simplify their research workflow, provide visual reports and checkpoints, and engender trust in the tool itself.
The *NiPreps* framework extends *fMRIPrep*'s approach and principles to new imaging modalities.
The vision for *NiPreps* is to provide end-users (i.e., researchers) with applications that allow them to perform quality control smoothly and to prepare their data for modeling and statistical analysis.

## Leveraging BIDS

*NiPreps* leverage the [Brain Imaging Data Structure (BIDS)](../apps/framework.md#what-is-bids) to understand all the particular
features and available metadata (i.e., imaging parameters) of the input dataset.
BIDS allows *NiPreps* to automatically stage the most adequate preprocessing workflow while minimizing manual intervention.

## Architecture

The *NiPreps* framework (Figure 1) encompasses a wide array of software projects organized into three layers of scientific software:

  * **Software infrastructure**: including quite mature projects such as [*NiPype*][2] and [*NiBabel*][3]; the standard specifications of the Brain Imaging Data Structure (BIDS, and BIDS-Derivatives); and some other tools such as *NiTransforms* or *TemplateFlow*, under development.
    These tools deliver low-level interfaces (e.g., data access to images and spatial transforms) and utilities (see Figure 1).
  * **Middleware**: these are utilities that generalize their functionalities across the end-user tools.
    These utilities cover foundational processing methodologies (e.g., [*NiWorkflows*][4] and [*SDCflows*][5]), the crowdsourcing of metadata (e.g., *MRIQC Web-API*), and the support for deep learning models (*MRIQC-nets*).
  * **End-user tools such as *fMRIPrep***: Some existing end-user tools include *sMRIPrep (Structural MRI Preprocessing)*, which lies in between an end-user tool and middleware, as it is involved in higher-level tools such as *fMRIPrep*. Finally, quality control tools (e.g., *MRIQC*) to be executed before any preprocessing happens.

## Projects

  * [*fMRIPrep*][1] ([GitHub](https://github.com/poldracklab/fmriprep)): fMRI Preprocessing
  * [*dMRIPrep*][6] ([GitHub](https://github.com/nipreps/dmriprep)): dMRI Preprocessing
  * [*sMRIPrep*][7] ([GitHub](https://github.com/poldracklab/smriprep)): Structural MRI Preprocessing
  * [*MRIQC*][8] ([GitHub](https://github.com/poldracklab/mriqc)): MRI quality control
  * [*SDCflows*][5] ([GitHub](https://github.com/nipreps/sdcflows)): Susceptibility-derived distortion correction (SDC) workflows
  * [*NiWorkflows*][4] ([GitHub](https://github.com/nipreps/niworkflows)): General/miscellaneous workflow utilities
  * [*TemplateFlow*][9]: A registry of neuroimaging templates and spatial mappings between them.

<!-- ![Branching](https://guides.github.com/activities/hello-world/branching.png) -->

[1]: http://fmriprep.org/ "fMRIPrep documentation"
[2]: https://nipype.readthedocs.io/ "NiPype documentation"
[3]: https://nibabel.readthedocs.io/ "NiBabel documentation"
[4]: https://www.nipreps.org/niworkflows/ "NiWorkflows documentation"
[5]: https://www.nipreps.org/sdcflows/ "SDCflows documentation"
[6]: https://www.nipreps.org/dmriprep/ "dMRIPrep documentation"
[7]: https://poldracklab.github.io/smriprep "sMRIPrep documentation"
[8]: https://mriqc.readthedocs.io/ "MRIQC Documentation"
[9]: https://www.templateflow.org/ "TemplateFlow"
