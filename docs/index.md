The current neuroimaging workflow has matured into a large chain of processing and analysis steps involving a large number of experts, across imaging modalities and applications.
The development and fast adoption of [_fMRIPrep_][1] have revealed that neuroscientists need tools that simplify their research workflow, provide visual reports and checkpoints, and engender trust in the tool itself.
The _NiPreps (NeuroImaging Preprocessing toolS)_ framework extends _fMRIPrep_'s approach and principles to new imaging modalities.
The vision for _NiPreps_ is to provide end-users (i.e., researchers) with applications that allow them to perform quality control smoothly and to prepare their data for modeling and statistical analysis.

## Projects

  * [_fMRIPrep_][1] ([GitHub](https://github.com/poldracklab/fmriprep)): fMRI Preprocessing
  * [_dMRIPrep_][6] ([GitHub](https://github.com/nipreps/dmriprep)): dMRI Preprocessing
  * [_sMRIPrep_][7] ([GitHub](https://github.com/poldracklab/smriprep)): Structural MRI Preprocessing
  * [_MRIQC_][8] ([GitHub](https://github.com/poldracklab/mriqc)): MRI quality control
  * [_SDCflows_][5] ([GitHub](https://github.com/nipreps/sdcflows)): Susceptibility-derived distortion correction (SDC) workflows
  * [_NiWorkflows_][4] ([GitHub](https://github.com/nipreps/niworkflows)): General/miscellaneous workflow utilities
  * [_TemplateFlow_][9]: A registry of neuroimaging templates and spatial mappings between them.

## Overview of the framework

The _NiPreps_ framework (Figure 1) encompasses a wide array of software projects organized into three layers of scientific software:

  * **Software infrastructure**: including quite mature projects such as [_NiPype_][2] and [_NiBabel_][3]; the standard specifications of the Brain Imaging Data Structure (BIDS, and BIDS-Derivatives); and some other tools such as _NiTransforms_ or _TemplateFlow_, under development.
    These tools deliver low-level interfaces (e.g., data access to images and spatial transforms) and utilities (see Figure 1).
  * **Middleware**: these are utilities that generalize their functionalities across the end-user tools.
    These utilities cover foundational processing methodologies (e.g., [_NiWorkflows_][4] and [_SDCflows_][5]), the crowdsourcing of metadata (e.g., _MRIQC Web-API_), and the support for deep learning models (_MRIQC-nets_).
  * **End-user tools such as _fMRIPrep_**: Some existing end-user tools include _sMRIPrep (Structural MRI Preprocessing)_, which lies in between an end-user tool and middleware, as it is involved in higher-level tools such as _fMRIPrep_. Finally, quality control tools (e.g., _MRIQC_) to be executed before any preprocessing happens.

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
