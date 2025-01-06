!!! abstract "Summary"

    Executing *BIDS-Apps* leveraging *DataLad*-controlled datasets
    within containers can be tricky.
    In particular, one of our general recommendations involves mounting
    or binding folders into the container in **read-only mode**, which
    will disallow *DataLad* from writing to the dataset tree.
    Similarly, and depending on the specific runtime settings of the
    container framework, *DataLad* may encounter issues with file ownership too.
    This section guides users through ensuring smooth execution of
    *BIDS-Apps* on *DataLad*/*Git-annex*-managed datasets.

## *DataLad* and *Docker*

Apps may be able to identify if the input dataset is handled with
[*DataLad*](https://www.datalad.org/) or [*git-annex*](https://git-annex.branchable.com), and pull down linked data that has not
been fetched yet.
One example of one such application is *MRIQC*, and all the examples
on this documentation page will refer to it.

When executing *MRIQC* within *Docker* on a *DataLad* dataset
(for instance, installed from [*OpenNeuro*](https://openneuro.org)),
we will need to ensure the following settings are observed:

* the user id (uid) who *installed* the *DataLad* dataset must match
  the uid who is *executing MRIQC* within the container runtime
* the uid who is *executing MRIQC* within the container must
  have sufficient permissions to write in the tree.

### Setting a regular user's execution uid

If the execution uid does not match the uid of the user who installed
the *DataLad* dataset, we will likely encounter the following error
with relatively recent
[*Git* versions (+2.35.2)](https://github.blog/open-source/git/git-security-vulnerability-announced/#):

```
datalad.runner.exception.CommandError: CommandError: 'git -c diff.ignoreSubmodules=none -c core.quotepath=false -c annex.merge-annex-branches=false annex find --not --in . --json --json-error-messages -c annex.dotfiles=true -- sub-0001/func/sub-0001_task-restingstate_acq-mb3_bold.nii.gz sub-0002/func/sub-0002_task-emomatching_acq-seq_bold.nii.gz sub-0002/func/sub-0002_task-restingstate_acq-mb3_bold.nii.gz sub-0001/func/sub-0001_task-emomatching_acq-seq_bold.nii.gz sub-0001/func/sub-0001_task-faces_acq-mb3_bold.nii.gz sub-0001/dwi/sub-0001_dwi.nii.gz sub-0002/func/sub-0002_task-workingmemory_acq-seq_bold.nii.gz sub-0001/anat/sub-0001_T1w.nii.gz sub-0002/anat/sub-0002_T1w.nii.gz sub-0001/func/sub-0001_task-gstroop_acq-seq_bold.nii.gz sub-0002/func/sub-0002_task-faces_acq-mb3_bold.nii.gz sub-0002/func/sub-0002_task-anticipation_acq-seq_bold.nii.gz sub-0002/dwi/sub-0002_dwi.nii.gz sub-0001/func/sub-0001_task-anticipation_acq-seq_bold.nii.gz sub-0001/func/sub-0001_task-workingmemory_acq-seq_bold.nii.gz sub-0002/func/sub-0002_task-gstroop_acq-seq_bold.nii.gz' failed with exitcode 1 under /data [info keys: stdout_json] [err: 'git-annex: Git refuses to operate in this repository, probably because it is owned by someone else.

To add an exception for this directory, call:
git config --global --add safe.directory /data

git-annex: automatic initialization failed due to above problems']
```

Confusingly, following the suggestion from *DataLad*
(just propagated from *Git*) of executing
`git config --global --add safe.directory /data` will not work in this
case, because this line must be executed within the container.
However, containers are *transient* and the setting this configuration
on *Git* will not be propagated between executions unless advanced
actions are taken (such as mounting a *HOME* folder with the necessary settings).

Instead, we can override the default user executing within the container
(which is `root`, or uid = 0).
Let's update the last example in the previous
[*Docker* execution section](docker.md#running-a-niprep-directly-interacting-with-the-docker-engine):


``` {.shell hl_lines="5"}
$ docker run -ti --rm \
    -v $HOME/ds002785:/data:ro \
    -v $HOME/ds002785/derivatives:/out \
    -v $HOME/tmp/ds002785-workdir:/work \
    -u $(id -u):$(id -g) \                   # set execution uid:gid
    nipreps/mriqc:<latest-version> \
    \
    /data /out/mriqc-<latest-version> \
    participant \
    -w /work
```

The above command line will ensure *MRIQC* to be executed with the current
uid and gid, which will match the filesystem's permissions if the dataset
was installed with the same user.

!!! danger "Match uid and gid with those corresponding to the user who installed the dataset"

    When different users are to install the dataset and
    execute the application, *Docker* must be executed with the
    uid and gid corresponding to the user who installed the dataset.
    The uid corresponding to a given username (for instance `janedoe`)
    can be obtained as follows:

    ```
    getent passwd "janedoe" | cut -f 3 -d ":"
    ```

    and her gid:

    ```
    getent passwd "janedoe" | cut -f 4 -d ":"
    ```

### Mounting the dataset folder without *read-only* permissions

If the dataset is protected with *read-only* permissions, then *MRIQC*
will hit the following error
([see `nipreps/mriqc#1363`](https://github.com/nipreps/mriqc/issues/1363)):

```
get(error): sub-0001/func/sub-0001_task-restingstate_acq-mb3_bold.nii.gz (file) [git-annex: .git/annex/tmp: createDirectory: permission denied (Read-only file system)]
action summary:
  get (error: 1)
Traceback (most recent call last):
  File "/opt/conda/bin/mriqc", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/conda/lib/python3.11/site-packages/mriqc/cli/run.py", line 43, in main
    parse_args(argv)
  File "/opt/conda/lib/python3.11/site-packages/mriqc/cli/parser.py", line 658, in parse_args
    initialize_meta_and_data()
  File "/opt/conda/lib/python3.11/site-packages/mriqc/utils/misc.py", line 447, in initialize_meta_and_data
    _datalad_get(dataset)
  File "/opt/conda/lib/python3.11/site-packages/mriqc/utils/misc.py", line 282, in _datalad_get
    return get(
           ^^^^
  File "/opt/conda/lib/python3.11/site-packages/datalad/interface/base.py", line 773, in eval_func
    return return_func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/lib/python3.11/site-packages/datalad/interface/base.py", line 763, in return_func
    results = list(results)
              ^^^^^^^^^^^^^
  File "/opt/conda/lib/python3.11/site-packages/datalad_next/patches/interface_utils.py", line 287, in _execute_command_
    raise IncompleteResultsError(
datalad.support.exceptions.IncompleteResultsError: Command did not complete successfully. 1 failed:
[{'action': 'get',
  'annexkey': 'MD5E-s76037251--344f061a3165c71e36b98ad1649c3c8c.nii.gz',
  'error_message': 'git-annex: .git/annex/tmp: createDirectory: permission '
                   'denied (Read-only file system)',
  'path': '/data/sub-0001/func/sub-0001_task-restingstate_acq-mb3_bold.nii.gz',
  'refds': '/data',
  'status': 'error',
  'type': 'file'}]
```

This error indicates that the container is executed with
the appropriate uid and gid pair.
In this case, we will need to ensure *DataLad* can write
to the dataset installation when obtaining new data.
This is easily achieved by **removing the read-only parameters** of the
mount option:

``` {.shell hl_lines="2 5"}
$ docker run -ti --rm \
    -v $HOME/ds002785:/data \                # mount data WITHOUT :ro
    -v $HOME/ds002785/derivatives:/out \
    -v $HOME/tmp/ds002785-workdir:/work \
    -u $(id -u):$(id -g) \                   # set execution uid:gid
    nipreps/mriqc:<latest-version> \
    \
    /data /out/mriqc-<latest-version> \
    participant \
    -w /work
```

## *DataLad* and *Singularity*/*Apptainer*

In the case of *Singularity* and *Apptainer*, ensuring the uid that
executes the container [involves using user namespace mappings](https://apptainer.org/docs/admin/1.0/user_namespace.html#user-namespace-requirementsn).
Therefore, you will need to contact your system administrator to figure
out a convenient solution to the problem.

Since most of *Singularity*/*Apptainer* deployments automatically bind
the user's `$HOME` directory, *DataLad*'s suggested direction may
work:

```
git config --global --add safe.directory <path-to-dataset-in-host>
```

Allowing the container to write on the dataset's tree is straightforward
and homologous to *Docker*, by removing the `:ro` setting in the binding
option (`-B`).
