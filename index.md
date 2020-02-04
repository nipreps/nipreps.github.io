---
layout: default
---

The current neuroimaging workflow has matured into a large chain of processing and analysis steps involving a large number of experts, across imaging modalities and applications.
The development and fast adoption of [_fMRIPrep_][1] have revealed that neuroscientists need tools that simplify their research workflow, provide visual reports and checkpoints, and engender trust in the tool itself.
The _NiPreps (NeuroImaging Preprocessing toolS)_ framework extends _fMRIPrep_'s approach and principles to new imaging modalities.
The vision for _NiPreps_ is to provide end-users (i.e., researchers) with applications that allow them to perform quality control smoothly and to prepare their data for modeling and statistical analysis.


# Overview of the framework

The _NiPreps_ framework (Figure 1) encompasses a wide array of software projects organized into three layers of scientific software:

  * **Software infrastructure**: including quite mature projects such as [_NiPype_][2] and [_NiBabel_][3]; the standard specifications of the Brain Imaging Data Structure (BIDS [3], and BIDS-Derivatives); and some other tools such as _NiTransforms_ or _TemplateFlow_, under development.
    These tools deliver low-level interfaces (e.g., data access to images and spatial transforms) and utilities (see Figure 1).
  * **Middleware**: these are utilities that generalize their functionalities across the end-user tools.
    These utilities cover foundational processing methodologies (e.g., _NiWorkflows_ and _SDCFlows_), the crowdsourcing of metadata (e.g., _MRIQC Web-API_ [4]), and the support for deep learning models (_MRIQC-nets_).
  * **End-user tools such as _fMRIPrep_**: Some existing end-user tools include _sMRIPrep (Structural MRI Preprocessing)_, which lies in between an end-user tool and middleware, as it is involved in higher-level tools such as _fMRIPrep_. Finally, quality control tools (e.g., _MRIQC_ [5]) to be executed before any preprocessing happens.

<!-- ![Branching](https://guides.github.com/activities/hello-world/branching.png) -->

# Principles of end-user _NiPreps_

#. _NiPreps_ only and fully support BIDS and BIDS-Derivatives for the input and output data.
#. _NiPreps_ are packaged as a fully-compliant BIDS-Apps [6], not just in its user interface, but also in the continuous integration, testing, and delivery.
#. The scope of _NiPreps_ is strictly limited to preprocessing tasks.
#. _NiPreps_ are agnostic to subsequent analysis, i.e., any software supporting BIDS-Derivatives for its inputs should be amenable to analyze data preprocessed with them.
#. _NiPreps_ are thoroughly and transparently documented (including the generation of individual, visual reports with a consistent format that serve as scaffolds for understanding the underpinnings and design decisions).
#. _NiPreps_ are community-driven, and contributors (in any sense) always get credited with authorship within relevant publications.
#. _NiPreps_ are modular, reliant on widely-used tools such as _AFNI_, _ANTs_, _FreeSurfer_, _FSL_, _NiLearn_, or _DIPY_ [7-12] and extensible via plug-ins.


[1]: http://fmriprep.org/ "fMRIPrep documentation"
[2]: https://nipype.readthedocs.io/ "NiPype documentation"
[3]: https://nibabel.readthedocs.io/ "NiBabel documentation"
