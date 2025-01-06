!!! abstract "Summary"

    Here, we describe how to run *NiPreps* with Docker containers.
    To illustrate the process, we will show the execution of *fMRIPrep*, but these guidelines extend to any other end-user *NiPrep*.

## Before you start: install Docker

Probably, the most popular framework to execute containers is Docker.
If you are to run a *NiPrep* on your PC/laptop, this is the **RECOMMENDED** way of execution.
Please make sure you follow the Docker installation instructions.
You can check your Docker Runtime installation running their `hello-world` image:

```Shell
$ docker run --rm hello-world
```

If you have a functional installation, then you should obtain the following output:

```Shell
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

After checking your Docker Engine is capable of running Docker images, you are ready to pull your first *NiPreps* container image.

!!! tip "Troubleshooting"

    If you encounter issues while executing a containerized application,
    it is critical to identify where the fault is sourced.
    For issues emerging from the *Docker Engine*, please read the
    [corresponding troubleshooting guidelines](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/#volumes).
    Once verified the problem is not related to the container system,
    then follow the specific application debugging guidelines.

## Docker images

For every new version of the particular *NiPrep* app that is released, a corresponding Docker image is generated.
The Docker image *becomes* a container when the execution engine loads the image and adds an extra layer that makes it *runnable*. In order to run *NiPreps* Docker images, the Docker Runtime must be installed.
<!-- (see `installation_docker`{.interpreted-text
role="ref"}).-->

Taking *fMRIPrep* to illustrate the usage, first you might want to make sure of the exact version of the tool to be used:

``` Shell
$ docker pull nipreps/fmriprep:<latest-version>
```

You can run *NiPreps* interacting directly with the Docker Engine via the `docker run` interface.


## Running a *NiPrep* with a lightweight wrapper

Some *NiPreps* include a lightweight wrapper script for convenience.
That is the case of *fMRIPrep* and its `fmriprep-docker` wrapper.
Before starting, make sure you [have the wrapper installed](https://fmriprep.readthedocs.io/en/latest/installation.html#the-fmriprep-docker-wrapper).
When you run `fmriprep-docker`, it will generate a Docker command line for you, print it out for reporting purposes, and then execute it without further action needed, e.g.:

``` Shell
$ fmriprep-docker /path/to/data/dir /path/to/output/dir participant
RUNNING: docker run --rm -it -v /path/to/data/dir:/data:ro \
    -v /path/to_output/dir:/out nipreps/fmriprep:20.2.2 \
    /data /out participant
...
```

`fmriprep-docker` implements [the unified command-line interface of BIDS Apps](framework.md#a-unified-command-line-interface), and automatically translates directories into Docker mount points for you.

We have published a [step-by-step tutorial](http://reproducibility.stanford.edu/fmriprep-tutorial-running-the-docker-image/) illustrating how to run `fmriprep-docker`.
This tutorial also provides valuable troubleshooting insights and advice on what to do after
*fMRIPrep* has run.

## Running a *NiPrep* directly interacting with the Docker Engine

If you need a finer control over the container execution, or you feel comfortable with the Docker Engine, avoiding the extra software layer of the wrapper might be a good decision.

### Accessing filesystems in the host within the container

Containers are confined in a sandbox, so they can't access the host
in any ways unless you explicitly prescribe acceptable accesses
to the host.
The Docker Engine provides mounting filesystems into the container with the `-v` argument and the following syntax:
`-v some/path/in/host:/absolute/path/within/container:ro`,
where the trailing `:ro` specifies that the mount is read-only.
The mount permissions modifiers can be omitted, which means the mount
will have read-write permissions.

!!! warning "*Docker for Windows* requires enabling Shared Drives"

    On *Windows* installations, the `-v` argument will not work
    by default because it is necessary to enable shared drives.
    Please check on this [Stackoverflow post](https://stackoverflow.com/a/51822083) how to enable them.

In general, you'll want to at least provide two mount-points:
one set in read-only mode for the input data and one read/write
to store the outputs:

``` {.shell hl_lines="2 3"}
$ docker run -ti --rm \
    -v path/to/data:/data:ro \        # read-only, for data
    -v path/to/output:/out \          # read-write, for outputs
    nipreps/fmriprep:<latest-version> \
    /data /out/out \
    participant
```

When **debugging** or **reusing pre-cached intermediate results**,
you'll also need to mount some working directory that otherwise
is not exposed by the application.
In the case of *NiPreps*, we typically inform the *BIDS Apps*
to override the work directory by setting the `-w`/`--work-dir`
argument (please note that this is not defined by the *BIDS Apps*
specifications and it may change across applications):

``` {.shell hl_lines="4 8"}
$ docker run -ti --rm \
    -v path/to/data:/data:ro \
    -v path/to/output:/out \
    -v path/to/work:/work \              # mount from host
    nipreps/fmriprep:<latest-version> \
    /data /out/out \
    participant
    -w /work                             # override default directory
```

!!! tip "Best practices"

    The [*ReproNim* initiative](https://www.repronim.org/)
    distributes materials and documentation of best practices
    for containerized execution of neuroimaging workflows.
    Most of these are organized within the
    [*YODA* (Yoda's Organigram on Data Analysis)](https://github.com/myyoda) principles.

    For example, mounting `$PWD` into `$PWD` and setting that path
    as current working directory can effectively resolve many issues.
    This strategy may be combined with the above suggestion about
    the application's work directory as follows:

    ``` {.shell hl_lines="4 5 9"}
    $ docker run -ti --rm \
        -v path/to/data:/data:ro \
        -v path/to/output:/out \
        -v $PWD:$PWD \
        -w $PWD \   # DO NOT confuse with the application's work directory
        nipreps/fmriprep:<latest-version> \
        /data /out/out \
        participant
        -w $PWD/work
    ```

    Mounting `$PWD` may be used with YODA so that all necessary *parts*
    in execution are reachable from under `$PWD`.
    This effectively
    (i) makes it easy to *transfer* configurations from
    *outside* the container to the *inside* execution runtime;
    (ii) the *outside*/*inside* filesystem trees are homologous, which
    makes post-processing and orchestration easier;
    (iii) execution in shared systems is easier as everything is
    sort of *self-contained*.

    In addition to mounting `$PWD`, other advanced practices
    include mounting specific configuration files (for example, a
    [*Nipype* configuration file](https://miykael.github.io/nipype_tutorial/notebooks/basic_execution_configuration.html))
    into the appropriate paths within the container.


*BIDS Apps* relying on [*TemplateFlow*](https://www.templateflow.org)
for atlases and templates management may require
the *TemplateFlow Archive* be mounted from the host.
Mounting the *Archive* from the host is an effective way
to preempt the download of your favorite templates in every run:

``` {.shell hl_lines="5 6"}
$ docker run -ti --rm \
    -v path/to/data:/data:ro \
    -v path/to/output:/out \
    -v path/to/work:/work \
    -v path/to/tf-cache:/opt/templateflow \  # mount from host
    -e TEMPLATEFLOW_HOME=/opt/templateflow \ # override TF home
    nipreps/fmriprep:<latest-version> \
    /data /out/out \
    participant
    -w /work
```

!!! danger "Sharing the *TemplateFlow* cache can cause race conditions in parallel execution"

    When sharing the *TemplateFlow* *HOME* folder across several parallel
    executions against a single filesystem, these instance will likely
    attempt to fetch unavailable templates without sufficient time between
    actions for the data to be fully downloaded (in other words,
    data downloads will be *racing* each other).

    To resolve this issue, you will need to make sure all necessary
    templates are already downloaded within the cache folder.
    If the *TemplateFlow Client* is properly installed in your system,
    this is possible with the following command line
    (example shows how to fully download `MNI152NLin2009cAsym`:

    ``` Shell
    $ templateflow get MNI152NLin2009cAsym
    ```

### Running containers as a user

By default, Docker will run the container with the
user id (uid) **0**, which is reserved for the default **root**
account in *Linux*.
In other words, by default *Docker* will use the superuser account
to execute the container and will write files with the corresponding
uid=0 unless configured otherwise.
Executing as superuser may derive in permissions and security issues,
for example, [with *DataLad* (discussed later)](datalad.md#).
One paramount example of permissions issues where beginners typically
run into is deleting files after a containerized execution.
If the uid is not overridden, the outputs of a containerized execution
will be owned by **root** and group **root**.
Therefore, normal users will not be able to modify the output and
superuser permissions will be required to deleted data generated
by the containerized application.
Some shared systems only allow running containers as a normal user
because the user will not be able to action on the outputs otherwise.

Either way (whether the container is available with default settings
or the execution has been customized to normal users),
running as a normal user allows preempting these permissions issues.
This can be achieved with
[*Docker*'s `-u`/`--user` option](https://docs.docker.com/engine/containers/run/#user):

```
--user=[ user | user:group | uid | uid:gid | user:gid | uid:group ]
```

We can combine this option with *Bash*'s `id` command to ensure the current user's uid and group id (gid) are being set:

``` {.shell hl_lines="4"}
$ docker run -ti --rm \
    -v path/to/data:/data:ro \
    -v path/to/output:/out \
    -u $(id -u):$(id -g) \                   # set execution uid:gid
    -v path/to/tf-cache:/opt/templateflow \  # mount from host
    -e TEMPLATEFLOW_HOME=/opt/templateflow \ # override TF home
    nipreps/fmriprep:<latest-version> \
    /data /out/out \
    participant
```

For example:

``` Shell
$ docker run -ti --rm \
    -v $HOME/ds005:/data:ro \
    -v $HOME/ds005/derivatives:/out \
    -v $HOME/tmp/ds005-workdir:/work \
    -u $(id -u):$(id -g) \
    -v $HOME/.cache/templateflow:/opt/templateflow \
    -e TEMPLATEFLOW_HOME=/opt/templateflow \
    nipreps/fmriprep:<latest-version> \
    /data /out/fmriprep-<latest-version> \
    participant \
    -w /work
```

### Application-specific options

Once the Docker Engine arguments are written, the remainder of the
command line follows the interface defined by the specific
*BIDS App* (for instance,
[*fMRIPrep*](https://fmriprep.readthedocs.io/en/latest/usage.html)
or [*MRIQC*](https://mriqc.readthedocs.io/en/latest/running.html#command-line-interface)).

The first section of a call comprehends arguments specific to *Docker*,
and configure the execution of the container:

``` {.shell hl_lines="1-7"}
$ docker run -ti --rm \
    -v $HOME/ds005:/data:ro \
    -v $HOME/ds005/derivatives:/out \
    -v $HOME/tmp/ds005-workdir:/work \
    -u $(id -u):$(id -g) \
    -v $HOME/.cache/templateflow:/opt/templateflow \
    -e TEMPLATEFLOW_HOME=/opt/templateflow \
    nipreps/fmriprep:<latest-version> \
    /data /out/fmriprep-<latest-version> \
    participant \
    -w /work
```

Then, we specify the container image that we execute:

``` {.shell hl_lines="8"}
$ docker run -ti --rm \
    -v $HOME/ds005:/data:ro \
    -v $HOME/ds005/derivatives:/out \
    -v $HOME/tmp/ds005-workdir:/work \
    -u $(id -u):$(id -g) \
    -v $HOME/.cache/templateflow:/opt/templateflow \
    -e TEMPLATEFLOW_HOME=/opt/templateflow \
    nipreps/fmriprep:<latest-version> \
    /data /out/fmriprep-<latest-version> \
    participant \
    -w /work
```

Finally, the application-specific options can be added.
We already described the work directory setting before, in the case
of *NiPreps* such as *MRIQC* and *fMRIPrep*.
Some options are *BIDS Apps* standard, such as
the *analysis level* (`participant` or `group`)
and specific participant identifier(s) (`--participant-label`):

``` {.shell hl_lines="9-12"}
$ docker run -ti --rm \
    -v $HOME/ds005:/data:ro \
    -v $HOME/ds005/derivatives:/out \
    -v $HOME/tmp/ds005-workdir:/work \
    -u $(id -u):$(id -g) \
    -v $HOME/.cache/templateflow:/opt/templateflow \
    -e TEMPLATEFLOW_HOME=/opt/templateflow \
    nipreps/fmriprep:<latest-version> \
    /data /out/fmriprep-<latest-version> \
    participant \
    --participant-label 001 002 \
    -w /work
```

### Resource constraints

*Docker* may be executed with limited resources.
Please [read the documentation](https://docs.docker.com/engine/containers/resource_constraints/)
to limit resources such as memory, memory policies, number of CPUs, etc.

**Memory will be a common culprit** when working with large datasets
(+10GB).
However, *Docker* engine is limited to 2GB of RAM by default
for some installations of *Docker* for *MacOSX* and *Windows*.
The general resource settings can be also modified through the *Docker Desktop*
graphical user interface.
On a shell, the memory limit can be overridden with:

```
$ service docker stop
$ dockerd --storage-opt dm.basesize=30G
```
