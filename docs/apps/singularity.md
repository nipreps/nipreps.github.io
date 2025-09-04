!!! important "Summary"

    Here, we describe how to run *NiPreps* with Singularity containers.
    To illustrate the process, we will show the execution of *fMRIPrep*, but these guidelines extend to any other end-user *NiPrep*.

!!! warning "Apptainer"
    In 2021, [*Singularity* was rebranded as *Apptainer* when the project was transferred to the Linux Foundation](https://apptainer.org/news/community-announcement-20211130/).
    As noted in the community announcement, all the commands below that contain `singularity` as the command line executable will execute *Apptainer* and can be replaced with the `apptainer` command with no change in function. 

## Preparing a Singularity image

**Singularity version >= 2.5**:
If the version of Singularity installed on your HPC (High-Performance Computing)
system is modern enough you can create Singularity image
directly on the system. This is as simple as:

``` Shell
$ singularity build /my_images/fmriprep-<version>.simg \
                    docker://nipreps/fmriprep:<version>
```

where `<version>` should be replaced with the desired version of
*fMRIPrep* that you want to download.

**Singularity version < 2.5**:
In this case, start with a machine (e.g., your personal computer) with
Docker installed. Use
[docker2singularity](https://github.com/singularityware/docker2singularity)
to create a singularity image. You will need an active internet
connection and some time:

```
$ docker run --privileged -t --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v D:\host\path\where\to\output\singularity\image:/output \
    singularityware/docker2singularity \
    nipreps/fmriprep:<version>
```

Where `<version>` should be replaced with the desired version of
*fMRIPrep* that you want to download.

Beware of the back slashes, expected for Windows systems. For \*nix
users the command translates as follows: :

```
$ docker run --privileged -t --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /absolute/path/to/output/folder:/output \
    singularityware/docker2singularity \
    nipreps/fmriprep:<version>
```

Transfer the resulting Singularity image to the HPC, for example, using
`scp` or `rsync`:

``` Shell
$ scp nipreps_fmriprep*.img user@hcpserver.edu:/my_images
```

## Running a Singularity Image

If the data to be preprocessed is also on the HPC, you are ready to run
the *NiPrep*:

``` Shell
$ singularity run --cleanenv fmriprep.simg \
    path/to/data/dir path/to/output/dir \
    participant \
    --participant-label label
```

## Handling environment variables

Singularity by default [exposes all environment variables from the host inside the container](https://github.com/apptainer/singularity/issues/445).
Because of this, your host libraries (e.g., [NiPype](https://nipype.readthedocs.io) or a Python environment) could be accidentally used instead of the ones inside the
container. To avoid such a situation, we strongly **recommend** using the
`--cleanenv` argument in all scenarios. For example:

``` Shell
$ singularity run --cleanenv fmriprep.simg \
  /work/04168/asdf/lonestar/ $WORK/lonestar/output \
  participant \
  --participant-label 387 --nthreads 16 -w $WORK/lonestar/work \
  --omp-nthreads 16
```

Alternatively, conflicts might be preempted and some problems mitigated
by unsetting potentially problematic settings, such as the `PYTHONPATH`
variable, before running:

``` Shell
$ unset PYTHONPATH; singularity run fmriprep.simg \
  /work/04168/asdf/lonestar/ $WORK/lonestar/output \
  participant \
  --participant-label 387 --nthreads 16 -w $WORK/lonestar/work \
  --omp-nthreads 16
```

It is possible to define environment variables scoped within the
container by using the `SINGULARITYENV_*` magic, in combination with
`--cleanenv`. For example, we can set the FreeSurfer license variable
(see [*fMRIPrep*'s documentation on this](https://fmriprep.readthedocs.io/en/latest/usage.html#the-freesurfer-license)) as follows: :

```Shell
$ export SINGULARITYENV_FS_LICENSE=$HOME/.freesurfer.txt
$ singularity exec --cleanenv fmriprep.simg env | grep FS_LICENSE
FS_LICENSE=/home/users/oesteban/.freesurfer.txt
```

As we can see, the export in the first line tells Singularity to set a
corresponding environment variable of the same name after dropping the
prefix `SINGULARITYENV_`.

## Accessing the host's filesystem

Depending on how Singularity is configured on your cluster it might or
might not automatically bind (mount or expose) host's folders to the
container (e.g., `/scratch`, or `$HOME`). This is particularly relevant
because, *if you can't run Singularity in privileged mode* (which is
almost certainly true in all the scenarios), **Singularity containers
are read only**. This is to say that you won't be able to write
*anything* unless Singularity can access the host's filesystem in write
mode.

By default, Singularity automatically binds (mounts) the user's *home*
directory and a *scratch* directory. In addition, Singularity generally
allows binding the necessary folders with the
`-B <host_folder>:<container_folder>[:<permissions>]` Singularity
argument. For example:

```Shell
$ singularity run --cleanenv -B /work:/work fmriprep.simg \
  /work/my_dataset/ /work/my_dataset/derivatives/fmriprep \
  participant \
  --participant-label 387 --nthreads 16 \
  --omp-nthreads 16
```

!!! warning

    If your Singularity installation doesn't allow you to bind non-existent
    bind points, you'll get an error saying
    `WARNING: Skipping user bind, non existent bind point (directory) in container`.
    In this scenario, you can either try to bind things onto some other bind
    point you know it exists in the image or rebuild your singularity image
    with `docker2singularity` as follows:

      ```
      $ docker run --privileged -ti --rm -v /var/run/docker.sock:/var/run/docker.sock \
               -v $PWD:/output singularityware/docker2singularity \
               -m "/gpfs /scratch /work /share /lscratch /opt/templateflow"
      ```

    In the example above, the following bind points are created: `/gpfs`,
    `/scratch`, `/work`, `/share`, `/opt/templateflow`.

!!! important

    One great feature of containers is their confinement or isolation from
    the host system. Binding mount points breaks this principle, as the
    container has now access to create changes in the host. Therefore, it is
    generally recommended to use binding scarcely and granting very limited
    access to the minimum necessary resources. In other words, it is
    preferred to bind just one subdirectory of `$HOME` than the full `$HOME`
    directory of the host (see [nipreps/fmriprep#1778 (comment)](https://github.com/nipreps/fmriprep/issues/1778\#issuecomment-538009563)).


**Relevant aspects of the** `$HOME` **directory within the container**:
By default, Singularity will bind the user's `$HOME` directory in the
host into the `/home/$USER` (or equivalent) in the container. Most of
the times, it will also redefine the `$HOME` environment variable and
update it to point to the corresponding mount point in `/home/$USER`.
However, these defaults can be overwritten in your system. It is
recommended to check your settings with your system's administrators.
If your Singularity installation allows it, you can workaround the
`$HOME` specification combining the bind mounts argument (`-B`) with the
home overwrite argument (`--home`) as follows:

```Shell
$ singularity run -B $HOME:/home/fmriprep --home /home/fmriprep \
      --cleanenv fmriprep.simg <fmriprep arguments>
```

## *TemplateFlow* and Singularity

[*TemplateFlow*](https://www.templateflow.org) is a helper tool that allows neuroimaging workflows to programmatically access a repository of standard neuroimaging templates.
In other words, *TemplateFlow* allows *NiPreps* to dynamically change
the templates that are used, e.g., in the atlas-based brain extraction
step or spatial normalization.

Default settings in the Singularity image should get along with the
*Singularity* installation of your system. However, deviations from the
default configurations of your installation may break this
compatibility. A particularly problematic case arises when the home
directory is mounted in the container, but the `$HOME` environment
variable is not correspondingly updated. Typically, you will experience
errors like `OSError: [Errno 30] Read-only file system` or
`FileNotFoundError: [Errno 2] No such file or directory: '/home/fmriprep/.cache'`.

If it is not explicitly forbidden in your installation, the first
attempt to overcome this issue is manually setting the `$HOME` directory
as follows:

```Shell
$ singularity run --home $HOME --cleanenv fmriprep.simg <fmriprep arguments>
```

If the user's home directory is not automatically bound, then the
second step would include manually binding it as in the section above: :

```Shell
$ singularity run -B $HOME:/home/fmriprep --home /home/fmriprep \
      --cleanenv fmriprep.simg <fmriprep arguments>
```

Finally, if the `--home` argument cannot be used, you'll need to
provide the container with writable filesystems where *TemplateFlow*'s
files can be downloaded. In addition, you will need to indicate
*fMRIPrep* to update the default paths with the new mount points setting
the `SINGULARITYENV_TEMPLATEFLOW_HOME` variable. :

```Shell
# Tell the NiPrep where TemplateFlow will place downloads
$ export SINGULARITYENV_TEMPLATEFLOW_HOME=/opt/templateflow
$ singularity run -B <writable-path-on-host>:/opt/templateflow \
      --cleanenv fmriprep.simg <fmriprep arguments>
```

## Restricted Internet access

We have identified several conditions in which running *NiPreps* might
fail because of spotty or impossible access to Internet.

If your compute node cannot have access to Internet, then you'll need
to pull down from TemplateFlow all the resources that will be necessary
ahead of run-time.

If that is not the case (i.e., you should be able to hit HTTP/s
endpoints), then you can try the following:

* `VerifiedHTTPSConnection ... Failed to establish a new connection: [Errno 110] Connection timed out`.
  If you encounter an error like this, probably you'll need to set up an
  http proxy exporting `SINGULARITYENV_http_proxy` (see [nipreps/fmriprep#1778 (comment)](https://github.com/nipreps/fmriprep/issues/1778\#issuecomment-532297622).
  For example:

    ```Shell
    $ export SINGULARITYENV_https_proxy=http://<ip or proxy name>:<port>
    ```

* `requests.exceptions.SSLError: HTTPSConnectionPool ...`. In this case,
  your container seems to be able to reach the Internet, but unable to use
  SSL encryption. There are two potential solutions to the issue. The
  [recommended one](https://neurostars.org/t/problems-using-pediatric-template-from-templateflow/4566/17)
  is setting `REQUESTS_CA_BUNDLE` to the appropriate path, and/or binding
  the appropriate filesystem:

    ```shell
    $ export SINGULARITYENV_REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
    $ singularity run -B <path-to-certs-folder>:/etc/ssl/certs \
          --cleanenv fmriprep.simg <fmriprep arguments>
    ```
  Otherwise, [some users have succeeded pre-fetching the necessary
  templates onto the *TemplateFlow* directory to then bind the folder at
  execution](https://neurostars.org/t/problems-using-pediatric-template-from-templateflow/4566/15):

    ```Shell
    $ export TEMPLATEFLOW_HOME=/path/to/keep/templateflow
    $ python -m pip install -U templateflow  # Install the client
    $ python
    >>> import templateflow.api
    >>> templateflow.api.TF_S3_ROOT = 'http://templateflow.s3.amazonaws.com'
    >>> api.get(‘MNI152NLin6Asym’)
    ```

Finally, run the singularity image binding the appropriate folder:

```Shell
$ export SINGULARITYENV_TEMPLATEFLOW_HOME=/templateflow
$ singularity run -B ${TEMPLATEFLOW_HOME:-$HOME/.cache/templateflow}:/templateflow \
      --cleanenv fmriprep.simg <fmriprep arguments>
```

## *Socket errors* when running parallel processes on HPC

When running multiple instances of a *NiPreps* on HPC, you may encounter
errors like [`nipreps/mriqc#1170`](https://github.com/nipreps/mriqc/issues/1170):

``` text
OSError: [Errno 98] Address already in use
```

To solve this issue, you can try to isolate the container network from
the host network by using the `--network none` setting of *Singularity*/*Apptainer*:

``` shell
apptainer run --net --network none ...
```

This solution prevents the container from accessing the Internet and from
downloading data, for example, templates.
Please follow the previous section's guidelines to pre-fetch templates
and then making them accessible.

## Troubleshooting

Setting up a functional execution framework with Singularity might be
tricky in some HPC (high-performance computing) systems.
Please make sure you have read the relevant
[documentation of Singularity](https://sylabs.io/docs/), and checked all the
defaults and configuration in your system. The next step is checking the
environment and access to *fMRIPrep* resources, using
`singularity shell`.

1. Check access to input data folder, and BIDS validity:
      ```Shell
      $ singularity shell -B path/to/data:/data fmriprep.simg
      Singularity fmriprep.simg:~> ls /data
      CHANGES  README  dataset_description.json  participants.tsv  sub-01  sub-02  sub-03  sub-04  sub-05  sub-06  sub-07  sub-08  sub-09  sub-10  sub-11  sub-12  sub-13  sub-14  sub-15  sub-16  task-balloonanalogrisktask_bold.json
      Singularity fmriprep.simg:~> bids-validator /data
         1: [WARN] You should define 'SliceTiming' for this file. If you don't provide this information slice time correction will not be possible. (code: 13 - SLICE_TIMING_NOT_DEFINED)
                ./sub-01/func/sub-01_task-balloonanalogrisktask_run-01_bold.nii.gz
                ./sub-01/func/sub-01_task-balloonanalogrisktask_run-02_bold.nii.gz
                ./sub-01/func/sub-01_task-balloonanalogrisktask_run-03_bold.nii.gz
                ./sub-02/func/sub-02_task-balloonanalogrisktask_run-01_bold.nii.gz
                ./sub-02/func/sub-02_task-balloonanalogrisktask_run-02_bold.nii.gz
                ./sub-02/func/sub-02_task-balloonanalogrisktask_run-03_bold.nii.gz
                ./sub-03/func/sub-03_task-balloonanalogrisktask_run-01_bold.nii.gz
                ./sub-03/func/sub-03_task-balloonanalogrisktask_run-02_bold.nii.gz
                ./sub-03/func/sub-03_task-balloonanalogrisktask_run-03_bold.nii.gz
                ./sub-04/func/sub-04_task-balloonanalogrisktask_run-01_bold.nii.gz
                ... and 38 more files having this issue (Use --verbose to see them all).
        Please visit https://neurostars.org/search?q=SLICE_TIMING_NOT_DEFINED for existing conversations about this issue.
      ```

1. Check access to output data folder, and whether you have write
   permissions
      ```Shell
      $ singularity shell -B path/to/data/derivatives/fmriprep-1.5.0:/out fmriprep.simg
      Singularity fmriprep.simg:~> ls /out
      Singularity fmriprep.simg:~> touch /out/test
      Singularity fmriprep.simg:~> rm /out/test
      ```

1.  Check access and permissions to `$HOME`:
      ```Shell
      $ singularity shell fmriprep.simg
      Singularity fmriprep.simg:~> mkdir -p $HOME/.cache/testfolder
      Singularity fmriprep.simg:~> rmdir $HOME/.cache/testfolder
      ```

1.  Check *TemplateFlow* operation:
      ```Shell
      $ singularity shell -B path/to/templateflow:/templateflow fmriprep.simg
      Singularity fmriprep.simg:~> echo ${TEMPLATEFLOW_HOME:-$HOME/.cache/templateflow}
      /home/users/oesteban/.cache/templateflow
      Singularity fmriprep.simg:~> python -c "from templateflow.api import get; get(['MNI152NLin2009cAsym', 'MNI152NLin6Asym', 'OASIS30ANTs', 'MNIPediatricAsym', 'MNIInfant'])"
         Downloading https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-01_atlas-HOCPA_desc-th0_dseg.nii.gz
         304B [00:00, 1.28kB/s]
         Downloading https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-01_atlas-HOCPA_desc-th25_dseg.nii.gz
         261B [00:00, 1.04kB/s]
         Downloading https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-01_atlas-HOCPA_desc-th50_dseg.nii.gz
         219B [00:00, 867B/s]
         ...
      ```

## Running Singularity on a SLURM system

An example of `sbatch` script to run *fMRIPrep* on a SLURM system[^1] is
given below. The submission script will
generate one task per subject using a *job array*.
```Shell
{!assets/fmriprep.slurm!}
```
Submission is then as easy as:

```Shell
$ export STUDY=/path/to/some/folder
$ sbatch --array=1-$(( $( wc -l $STUDY/data/participants.tsv | cut -f1 -d' ' ) - 1 )) fmriprep.slurm
```


[^1]: assuming that *job arrays* and Singularity are available
