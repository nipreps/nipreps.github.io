name: title
layout: true
class: center
---
layout: false
count: false

.middle.center[
# Building communities around reproducible workflows

<br />
<br />

### O. Esteban
#### CHUV | Lausanne University Hospital

###### [www.nipreps.org](https://www.nipreps.org)
]

---
layout: false
count: false

.middle.center[
# Building communities around reproducible workflows

<br />
<br />

### O. Esteban
#### CHUV | Lausanne University Hospital

###### [www.nipreps.org](https://www.nipreps.org)
]

???

I'm going to talk about how we are building a framework of preprocessing pipelines for neuroimaging called NiPreps, based on the fMRIPrep experience.
---
name: newsection
layout: true
class: section-separator

.perma-sidebar[
## Data Processing
### (Day 2, 15h CET)
# Workflows

<br />
<br />
<br />
<br />
<br />

<p align="center">
<img src="../nipreps-qr.svg" width="70%" />
</p>
<br />
<p align="center">
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
</p>
]

---
name: sidebar
layout: true

.perma-sidebar[
## Data Processing
### (Day 2, 15h CET)
# Workflows

<br />
<br />
<br />
<br />
<br />

<p align="center">
<img src="../nipreps-qr.svg" width="70%" />
</p>
<br />
<p align="center">
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
</p>
]

---
template: sidebar

## Neuroimaging is now mature
* many excellent tools available (from specialized to foundational)
  * large toolboxes (AFNI, ANTs/ITK, FreeSurfer, FSL, Nilearn, SPM, etc.)
  * workflow software (Nipype, Shellscripts, Nextflow, CWL)
  * container technology, CI/CD

* a wealth of prior knowledge (esp. about humans)

* LOTS of data acquired everyday

## Workflows - game's on!
* although many neuroimaging areas are still in search of methodological breakthroughs,

* challenges have moved on to the workflows:
  * workflows within traditional toolboxes - usually not flexible to adapt to new data
  * BIDS and BIDS-Apps.


???

* researchers have a large portfolio of image processing components readily available
* toolboxes with great support and active maintenance:
---
## New questions changing the focus:

### - **validity** (does the workflow actually work out?)
### - **transparency** (is it a black-box? how precise is reporting?)
### - **vibration** (how each tool choice & parameters affect overall?)
### - **throughput** (how much data/time can it possible take?)
### - **robustness** (can I use it on diverse studies?)
### - **evaluation** (what is it unique about the workflow, w.r.t. existing alternatives?)

---

## The garden of forking paths

<p align="center">
<img src="../assets/narps.png" width="800px" alt="NARPS Paper" />
</p>

(Botvinik-Nezer et al., 2020)

Around 50% of teams used fMRIPrep'ed inputs.

---

## The *fMRIPrep* story

### fMRIPrep produces analysis-ready data from diverse data
* minimal requirements ([BIDS-compliant](https://bids-standard.github.io/bids-validator/));
* *agnostic* to downstream steps of the workflow
  * produces [BIDS-Derivatives](https://bids-specification.readthedocs.io/en/stable/derivatives/introduction.html);
* robust against inhomogeneity of data across studies

???

fMRIPrep takes in a task-based or resting-state
functional MRI dataset in BIDS-format
and returns preprocessed data ready for analysis.

Preprocessed data can be used for a broad range of analysis, and they are
formatted following BIDS-Derivatives to maximize compatibility with:
  * major software packages (AFNI, FSL, SPM\*, etc.)
  * further temporal filtering and denoising: *fMRIDenoise*
  * any BIDS-Derivatives compliant tool (e.g., *FitLins*).

--

### fMRIPrep is a [BIDS-App](https://bids-apps.github.io) ([Gorgolewski, et al. 2017](https://doi.org/10.1371/journal.pcbi.1005209))
* adhered to modern software-engineering standards (CI/CD, containers)
* compatible interface with other BIDS-Apps
* optimized for automatic execution

???

fMRIPrep adopts the BIDS-App specifications.
That means the software is tested with every change to the codebase,
it also means that packaging, containerization, and deployment are also
automated and require tests to be passing.
BIDS-Apps are inter-operable (via BIDS-Derivatives),
and optimized for execution in HPC, Cloud, etc.

--

### Minimizes human intervention
* avoid error-prone parameters settings (read them from BIDS)
* adapts the workflow to the actual data available
  * while remaining flexible to some design choices (e.g., whether or not reconstructing surfaces or customizing target normalized standard spaces)

???

fMRIPrep minimizes human intervention because the user does not
need to fiddle with any parameters - they are obtained from the BIDS structure.
However, fMRIPrep does allow some flexibility to ensure the preprocessing meets the requirements of the intended analyses.

---

### *fMRIPrep* was not originally envisioned as a community project ...

(we just wanted a robust tool to automatically preprocess incoming data of OpenNeuro.org)

--


### ... but a community built up quickly around it

<br />

--

.pull-left[
## Why?

* Preprocessing of fMRI was in need for **division of labor**.

* Obsession with **transparency** made early-adopters confident of the recipes they were applying.

* **Responsiveness** to feedback.
]

.pull-right[
<p align="center">
<img src="../torw2020/assets/fmriprep-ga-viewers.png" width="400px" />
</p>
]


???

Preprocessing is a time-consuming effort, requires expertise converging imaging foundations & CS, typically addressed with legacy *in-house* pipelines.

On the right-hand side, you'll find the chart of unique visitors
to fmriprep.org, which is the documentation website.

---

## Key aspect: credit all direct contributors

<p align="center">
<img src="../assets/fmriprep-authors.png" width="700px" alt="fMRIPrep authors" />
</p>

--

## .. and indirect: *citation boilerplate*.

---


### Researchers want to spend more time on those areas most relevant to them
(probably not preprocessing...)

???

With the development of fMRIPrep we understood that
researchers don't want to waste their time on preprocessing
(except for researchers developing new preprocessing techniques).

--

### Writing *fMRIPrep* required a team of several experts in processing methods for neuroimaging, with a solid base on Computer Science.
(research programs just can't cover the neuroscience and the engineering of the whole workflow - we need to divide the labor)

???

The current neuroimaging workflow requires extensive knowledge in
sometimes orthogonal fields such as neuroscience and computer science.
Dividing the labor in labs, communities or individuals with the necessary
expertise is the fundamental for the advance of the whole field.

--

### Transparency helps against the risk of super-easy tools
(easy-to-use tools are risky because they might get a researcher very far with no idea whatsoever of what they've done)

???

There is an implicit risk in making things too easy to operate:

For instance, imagine someone who runs fMRIPrep on diffusion data by
tricking the BIDS naming into an apparently functional MRI dataset.
If fMRIPrep reached the end at all, the garbage at the output could be fed into
further tools, in a sort of a snowballing problem.

When researchers have access to the guts of the software and are given an opportunity to understand what's going on, the risk of misuse dips.

--

### Established toolboxes do not have incentives for compatibility
(and to some extent this is not necessarily bad, as long as they are kept well-tested and they embrace/help-develop some minimal standards)

???

AFNI, ANTs, FSL, FreeSurfer, SPM, etc. have comprehensive software validation tests,
methodological validation tests, stress tests, etc. - which pushed up their quality and made them fundamental for the field.

Therefore, it is better to keep things that way (although some minimal efforts towards convergence in compatibility are of course welcome)

---

## The *dMRIPrep* story

After the success of *fMRIPrep*, some neuroimagers asked "*when a diffusion MRI fMRIPrep?*"

## NeuroStars.org
(please note this down)

--


Same situation in the field of diffusion MRI:

### Image Processing: Possible Guidelines for the Standardization & Clinical Applications (J. Veraart)

(https://www.ismrm.org/19/program_files/MIS15.htm)

--

# Please join!

Joseph, M.; Pisner, D.; Richie-Halford, A.; Lerma-Usabiaga, G.; Keshavan, A.; Kent, JD.; Cieslak, M.; Poldrack, RA.; Rokem, A.; Esteban, O.

---

template: newsection
layout: false

.middle.center[
# www.nipreps.org

### (*NiPreps* == NeuroImaging PREProcessing toolS)

]

???

The enormous success of fMRIPrep led us to propose
its generalization to other MRI and non-MRI modalities,
as well as nonhuman species (for instance, rodents),
and particular populations currently unsupported by fMRIPrep
such as infants.

---

## Augmenting scanners to produce "*analysis-grade*" data
### (data *directly consumable* by analyses)

<br />
<br />

.pull-left[

***Analysis-grade* data** is an analogy to the concept of "*sushi-grade (or [sashimi-grade](https://en.wikipedia.org/wiki/Sashimi)) fish*" in that both are:

<br />

.large[**minimally preprocessed**,]

and

.large[**safe to consume** directly.]
]

.pull-right[
<img align="right" style='margin-right: 50px' src="https://1.bp.blogspot.com/-Osh4H4WXka0/WlMJmVgkZTI/AAAAAAAAEMY/GynUzSomJ-EBiyqv2m-maiOyKSM7SOmNACLcBGAs/s400/yellowfin%2Btuna%2Bsteaks%2Bnutrition.jpg" />
]

???

The goal, therefore, of NiPreps is to extend the scanner
so that, in a way, they produce data ready for analysis.

We liken these analysis-grade data to sushi-grade fish,
because in both cases the product is minimally preprocessed
and at the same time safe to consume as is.

---

template: newsection
layout: false

.middle.center[
# Deconstructing *fMRIPrep*

<br />

<img align="center" style="width: 60%" src="../torw2020/assets/deconstructing.png" />
]

???

For the last two years we've been decomposing the architecture of fMRIPrep, spinning off its constituent parts that are valuable in other applications.

This process of decoupling (to use a proper CS term) has been greatly facilitated by the modular nature of the code since its inception.

---

<div align="center" style='margin-top: 1em'>
<img alt="The NiPreps framework" src="../nipreps-chart.png" width="60%" />
</div>

???

The processing elements extracted from fMRIPrep can be mapped to three
regimes of responsibility:

- Software infrastructure composed by tools ensuring the collaboration and the most basic tooling.
- Middleware utilities, which build more advanced tooling based on the foundational infrastructure
- And at the top of the stack end-user applications - namely fMRIPrep, dMRIPrep, sMRIPrep and MRIQC.

As we can see, the boundaries of these three architectural layers are soft and tools such as TemplateFlow may stand in between.

Only projects enclosed in the brain shape pertain to the NiPreps community. NiPype, NiBabel and BIDS are so deeply embedded as dependencies that NiPreps can't be understood without them.

---

<img src="https://raw.githubusercontent.com/bids-standard/bids-specification/master/BIDS_logo/BIDS_logo_black.svg" width="20%" />

* BIDS provides a standard, guaranteeing I/O agreements:

  * Allows workflows to self-adapt to the inputs
  * Ensures the shareability of the results

* PyBIDS: a Python tool to query BIDS datasets ([Yarkoni et al., 2019](https://doi.org/10.21105/joss.01294)):

  ``` Python
  >>> from bids import BIDSLayout

  # Point PyBIDS to the dataset's path
  >>> layout = BIDSLayout("/data/coolproject")

  # List the participant IDs of present subjects
  >>> layout.get_subjects()
  ['01', '02', '03', '04', '05']

  # List session identifiers, if present
  >>> layout.get_sessions()
  ['01', '02']

  # List functional MRI tasks
  >>> layout.get_tasks()
  ['rest', 'nback']
  ```

???

BIDS is one of the keys to success for fMRIPrep and consequently, a strategic element of NiPreps.

Because the tools so far are written in Python, PyBIDS is a powerful tool to index and query inputs and outputs.

The code snippet illustrates the ease to find out the subject identifiers available in the dataset, sessions, and tasks.

---

## BIDS Derivatives

.cut-right[
``` Shell
derivatives/
├── fmriprep/
│ ├── dataset_description.json
│ ├── logs
│ ├── sub-01.html
│ ├── sub-01/
│ │ ├── anat/
│ │ │ ├── sub-01_desc-brain_mask.nii.gz
│ │ │ ├── sub-01_dseg.nii.gz
│ │ │ ├── sub-01_label-GM_probseg.nii.gz
│ │ │ ├── sub-01_label-WM_probseg.nii.gz
│ │ │ ├── sub-01_label-CSF_probseg.nii.gz
│ │ │ ├── sub-01_desc-preproc_T1w.nii.gz
│ │ │ ├── sub-01_space-MNI152_desc-brain_mask.nii.gz
│ │ │ ├── sub-01_space-MNI152_dseg.nii.gz
│ │ │ ├── sub-01_space-MNI152_label-GM_probseg.nii.gz
│ │ │ ├── sub-01_space-MNI152_label-WM_probseg.nii.gz
│ │ │ ├── sub-01_space-MNI152_label-CSF_probseg.nii.gz
│ │ │ ├── sub-01_space-MNI152_desc-preproc_T1w.nii.gz
│ │ │ ├── sub-01_from-MNI152_to-T1w_mode-image_xfm.h5
│ │ │ ├── sub-01_from-T1w_to-MNI152_mode-image_xfm.h5
│ │ │ └── sub-01_from-orig_to-T1w_mode-image_xfm.txt
│ │ ├── figures/
│ │ └── func/
│ │   ├── sub-01_task-rhymejudgment_space-MNI152_boldref.nii.gz
│ │   ├── sub-01_task-rhymejudgment_space-MNI152_desc-preproc_bold.nii.gz
│ │   ├── sub-01_task-rhymejudgment_space-MNI152_desc-confounds_regressors.nii.gz
│ │   └── sub-01_task-rhymejudgment_space-MNI152_desc-brain_mask.nii.gz
```
]


???

All NiPreps must write out BIDS-Derivatives.
As illustrated in the example, the outputs of fMRIPrep are very similar to the BIDS standard for acquired data.

---

## BIDS-Apps

* BIDS-Apps proposes a workflow structure model:

  <img src="../journal.pcbi.1005209.g002.png" width="85%" />

* Use of containers & CI/CD

* Uniform interface:
  .cut-right[
  ```Shell
  fmriprep /data /data/derivatives/fmriprep-20.1.1 participant [+OPTIONS]
  ```
  ]

???

All end-user applications in NiPreps must conform to the BIDS-Apps specifications.

The BIDS-Apps paper identified a common pattern in neuroimaging studies, where individual participants (and runs) are processed first individually, and then based on the outcomes, further levels of data aggregation are executed.

For this reason, BIDS-Apps define two major levels of execution: participant and group level.

Finally, the paper also stresses the importance of containerizing applications to ensure long-term preservation of run-to-run repeatability and proposes a common command line interface as described at the bottom:


- first the name of the BIDS-Apps (fmriprep, in this case)
- followed by input and output directories (respectively),
- to finally indicate the analysis level (always participant, for the case of fmriprep)

---

.pull-left[
<p align="center">
<img src="../card-nipype.svg" width="100%" />
</p>
<br />

``` Python
from nipype.interfaces.fsl import BET
brain_extract = BET(
  in_file="/data/coolproject/sub-01/ses-01/anat/sub-01_ses-01_T1w.nii",
  out_file="/out/sub-01/ses-01/anat/sub-01_ses-01_desc-brain_T1w.nii"
)
brain_extract.run()
```

Nipype is the gateway to mix-and-match from AFNI, ANTs, Dipy, FreeSurfer, FSL, MRTrix, SPM, etc.
]

.pull-right[
<p align="center">
<img src="https://nipype.readthedocs.io/en/latest/_images/nipype_architecture_overview2.png" width="60%" />
</p>
]


???

Nipype is the glue stitching together all the underlying neuroimaging toolboxes and provides the execution framework.

The snippet shows how the widely known BET tool from FSL can be executed using NiPype. This is a particular example instance of interfaces - which provide uniform access to the tooling with Python.

Finally, combining these interfaces we generate processing workflows to fulfill higher level processing tasks.

---

<img src="../card-nipype.svg" width="39%" />
<p align="center">
<img src="https://fmriprep.org/en/stable/_images/workflows-5.png" width="60%" />
</p>

???

For instance, we may have a look into fMRIPrep's functional processing block.

Nipype helps understand (and opens windows in the black box) generating these graph representation of the workflow.

---

<img src="../card-nibabel.svg" width="39%" />

``` Python
"""Fix the affine of a rodent dataset, imposing 0.2x0.2x0.2 [mm]."""
import numpy as np
import nibabel as nb

# Open the file
img = nb.load("sub-25_MGE_MouseBrain_3D_MGE_150.nii.gz")

# New (correct) affine
aff = np.diag((-0.2, -0.2, 0.2, 1.0))

# Use nibabel to reorient to canonical
card = nb.as_closest_canonical(nb.Nifti1Image(
    img.dataobj,
    np.diag((-0.2, -0.2, 0.2, 1.0)),
    None
))

# Save to disk
card.to_filename("sub-25_T2star.nii.gz")
```

???

NiBabel allows Python to easily access neuroimaging data formats such as NIfTI, GIFTI and CIFTI2.

Although this might be a trivial task, the proliferation of neuroimaging software has led to some sort of Wild West of formats, and sometimes interoperation is not ensured.

In the snippet, we can see how we can manipulate the orientation headers of a NIfTI volume, in particular a rodent image with incorrect affine information.
---

.pull-left[
<p align="center">
<img src="../card-nitransforms.svg" width="100%" />
</p>
<br />
<br />

Transforms typically are the outcome of image registration methodologies

<br />

The proliferation of software implementations of image registration methodologies has resulted in a spread of data structures and file formats used to preserve and communicate transforms.

([Esteban et al., 2020](https://doi.org/10.1109/ISBI45749.2020.9098466))
]

.pull-right[
<p align="center">
<img src="https://raw.githubusercontent.com/poldracklab/nitransforms/master/docs/_static/figure1-joss.png" width="90%" />
</p>
]


???

NiTransforms is a super-interesting toy project where we are exercising our finest coding skills.
It completes NiBabel in the effort of making spatial transforms calculated by neuroimaging software tools interoperable.

When it goes beyond the alpha state, it is expected to be merged into NiBabel.

At the moment, NiTransforms is already integrated in fMRIPrep +20.1
to concatenate LTA (linear affine transforms) transforms obtained with FreeSurfer,
ITK transforms obtained with ANTs, and motion parameters estimated with FSL.

Compatibility across formats is hard due to the many arbitrary decisions in establishing the mathematical framework of the transform and the intrinsic confusion of applying a transform.

While intuitively we understand applying a transform as "transforming the moving image so that I can represent it overlaid or fused with the reference image and both should look aligned", in reality, we only transform coordinates from the reference image into the moving image's space (step 1 on the right).

Once we know where the center of every voxel of the reference image falls in the moving image coordinate system, we read in the information (in other words, a value) from the moving image. Because the location will probably be off-grid, we interpolate such a value from the neighboring voxels (step 2).

Finally (step 3) we generate a new image object with the structure of the reference image and the data interpolated from the moving information. This new image object is the moving image "moved" on to the reference image space and thus, both look aligned.

---

.pull-left[
<p align="center">
<img src="../card-templateflow.svg" width="100%" />
</p>


* The Archive (right) is a repository of templates and atlases
* The Python Client (bottom) provides easy access (with lazy-loading) to the Archive

``` Python
>>> from templateflow import api as tflow
>>> tflow.get(
...     'MNI152NLin6Asym',
...     desc=None,
...     resolution=1,
...     suffix='T1w',
...     extension='nii.gz'
... )
PosixPath('/templateflow_home/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-01_T1w.nii.gz')
```

.large[www.templateflow.org]
]

.pull-right[
<p align="center">
<img src="../torw2020/assets/templateflow-archive.png" width="90%" />
</p>
]

???

One of the most ancient feature requests received from fMRIPrep early adopters was improving the flexibility of spatial normalization to standard templates other than fMRIPrep's default.

For instance, infant templates.

TemplateFlow offers an Archive of templates where they are stored, maintained and re-distributed;

and a Python client that helps accessing them.

On the right hand side, an screenshot of the TemplateFlow browser shows some of the templates currently available in the repository. The browser can be reached at www.templateflow.org.


The tool is based on PyBIDS, and the snippet will surely remind you of it.
In this case the example shows how to obtain the T1w template corresponding to FSL's MNI space, at the highest resolution.

If the files requested are not in TemplateFlow's cache, they will be pulled down and kept for further utilization.

---

## TemplateFlow - Archive
<p align="center">
<img src="../torw2020/assets/templateflow-datatypes.png" width="75%" />
</p>
.small[(Ciric et al. 2020, in prep)]

???

The Archive allows a rich range of data and metadata to be stored with the template.

Datatypes in the repository cover:

- images containing population-average templates,
- masks (for instance brain masks),
- atlases (including parcellations and segmentations)
- transform files between templates

Metadata can be stored with the usual BIDS options.

Finally, templates allow having multiple cohorts, in a similar encoding to that of multi-session BIDS datasets.

Multiple cohorts are useful, for instance, in infant templates with averages at several gestational ages.


---

<img src="../card-niworkflows.svg" width="39%" />

<br />
<br />

NiWorkflows is a miscellaneous mixture of tooling used by downstream *NiPreps*:

???

NiWorkflows is, historically, the first component detached from fMRIPrep.

For that reason, its scope and vision has very fuzzy boundaries as compared to the other tools.

The most relevant utilities incorporated within NiWorkflows are:

--

* The reportlet aggregation and individual report generation system

???

First, the individual report system which aggregates the visual elements or the reports (which we call "reportlets") and generates the final HTML document.

Also, most of the engineering behind the generation of these reportlets and their integration within NiPype are part of NiWorkflows

--

* Custom extensions to NiPype interfaces

???

Beyond the extension of NiPype to generate a reportlet from any given interface, NiWorkflows is the test bed for many utilities that are then upstreamed to nipype.

Also, special interfaces with a limited scope that should not be included in nipype are maintained here.

--

* Workflows useful across applications

???

Finally, NiWorkflows indeed offers workflows that can be used by end-user NiPreps. For instance atlas-based brain extraction of anatomical images, based on ANTs.

---

<img src="../card-sdcflows.svg" width="39%" />

<object style="width: 75%;" type="image/svg+xml" data="../torw2020/assets/sub-100068_task-machinegame_run-6_desc-sdc_bold.svg"></object>

???

Echo-planar imaging (EPI) are typically affected by distortions along the phase encoding axis, caused by the perturbation of the magnetic field at tissue interfaces.

Looking at the reportlet, we can see how in the "before" panel, the image is warped.

The distortion is most obvious in the coronal view (middle row) because this image has posterior-anterior phase encoding.

Focusing on the changes between "before" and "after" correction in this coronal view, we can see how the blue contours delineating the corpus callosum fit better the dark shade in the data after correction.

---

## Upcoming new utilities

### NiBabies | fMRIPrep-babies

* Mathias Goncalves

### NiRodents | fMRIPrep-rodents

* Eilidh MacNicol


???

So, what's coming up next?

NiBabies is some sort of NiWorkflows equivalent for the preprocessing of infant imaging. At the moment, only atlas-based brain extraction using ANTs (and adapted from NiWorkflows) is in active developments.

Next steps include brain tissue segmentation.

Similarly, NiRodents is the NiWorkflows parallel for the prepocessing of rodent preclinical imaging. Again, only atlas-based brain extraction adapted from NiWorkflows is being developed.

---

### *NiPreps* is a framework for the development of preprocessing workflows

* Principled design, with BIDS as an strategic component
* Leveraging existing, widely used software
* Using NiPype as a foundation

???

To wrap-up, I've presented NiPreps, a framework for developing preprocessing
workflows inspired by fMRIPrep.

The framework is heavily principle and tags along BIDS as a foundational component

NiPreps should not reinvent any wheel, trying to reuse as much as possible of the widely used and tested existing software.

Nipype serves as a glue components to orchestrate workflows.

--

### Why preprocessing?

* We propose to consider preprocessing as part of the image acquisition and reconstruction
* When setting the boundaries that way, it seems sensible to pursue some standardization in the preprocessing:
  * Less experimental degrees of freedom for the researcher
  * Researchers can focus on the analysis
  * More homogeneous data at the output (e.g., for machine learning)
* How:
  * Transparency is key to success: individual reports and documentation (open source is implicit).
  * Best engineering practices (e.g., containers and CI/CD)

???

But why just preprocessing, with a very strict scope?

We propose to think about preprocessing as part of the image acquisition and reconstruction process (in other words, scanning), rather than part of the analysis workflow.

This decoupling from analysis comes with several upshots:

First, there are less moving parts to play with for researchers in the attempt to fit their methods to the data (instead of fitting data with their methods).

Second, such division of labor allows the researcher to use their time in the analysis.

Finally, two preprocessed datasets from two different studies and scanning sites should be more homogeneous when processed with the same instruments, in comparison to processing them with idiosyncratic, lab-managed, preprocessing workflows.

However, for NiPreps to work we need to make sure the tools are transparent.

Not just with the individual reports and thorough documentation, also because of the community driven development. For instance, the peer-review process that goes around large incremental changes is fundamental to ensure the quality of the tool.

In addition, best engineering practices suggested in the BIDS-Apps paper, along with those we have been including with fMRIPrep, are necessary to ensure the quality of the final product.

--

### Challenges

* Testing / Validation!

???

As an open problem, validating the results of the tool remains extremely challenging for the lack in gold standard datasets that can tell us the best possible outcome.

---

## The *NMiND* story

NMiND = *NeverMIND, this Neuroimaging Method Is Not Duplicated*


### PIs worried about methodological duplicity

M. Milham, D. Fair, T. Satterthwaite, S. Ghosh, R. Poldrack, etc.

--

### NMiND's workgroups

*nosology* group, coding standards & patterns, sharing standards, testing standards, crediting contributors, funding strategy, benchmarking datasets.

### NMiND's nosology goals

* Consensus glossary of terms
* Landscape the portfolio of methodological solutions along several experimental and computational dimensions
* Organize and document a taxonomy along those dimensions
* Index existing software (from unit methods to workflows) in the taxonomy

Please Join!

---

template: newsection
layout: false

.middle.center[
# Thanks!

## Questions?
]
