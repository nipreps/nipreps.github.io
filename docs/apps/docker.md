!!! important "Summary"

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

## Docker images

For every new version of the particular *NiPrep* app that is released, a corresponding Docker image is generated.
The Docker image *becomes* a container when the execution engine loads the image and adds an extra layer that makes it *runnable*. In order to run *NiPreps* Docker images, the Docker Runtime must be installed.
<!-- (see `installation_docker`{.interpreted-text
role="ref"}).-->

Taking *fMRIPrep* to illustrate the usage, first you might want to make sure of the exact version of the tool to be used:

``` Shell
$ docker pull poldracklab/fmriprep:<latest-version>
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
    -v /path/to_output/dir:/out poldracklab/fmriprep:1.0.0 \
    /data /out participant
...
```

`fmriprep-docker` implements [the unified command-line interface of BIDS Apps](framework.md#a-unified-command-line-interface), and automatically translates directories into Docker mount points for you.

We have published a [step-by-step tutorial](http://reproducibility.stanford.edu/fmriprep-tutorial-running-the-docker-image/) illustrating how to run `fmriprep-docker`.
This tutorial also provides valuable troubleshooting insights and advice on what to do after
*fMRIPrep* has run.

## Running a *NiPrep* directly interacting with the Docker Engine

If you need a finer control over the container execution, or you feel comfortable with the Docker Engine, avoiding the extra software layer of the wrapper might be a good decision.

**Accessing filesystems in the host within the container**:
Containers are confined in a sandbox, so they can't access the host in any ways
unless you explicitly prescribe acceptable accesses to the host. The
Docker Engine provides mounting filesystems into the container with the
`-v` argument and the following syntax:
`-v some/path/in/host:/absolute/path/within/container:ro`, where the
trailing `:ro` specifies that the mount is read-only. The mount
permissions modifiers can be omitted, which means the mount will have
read-write permissions. In general, you'll want to at least provide two
mount-points: one set in read-only mode for the input data and one
read/write to store the outputs. Potentially, you'll want to provide
one or two more mount-points: one for the working directory, in case you
need to debug some issue or reuse pre-cached results; and a
[TemplateFlow](https://www.templateflow.org) folder to preempt the
download of your favorite templates in every run.

**Running containers as a user**:
By default, Docker will run the
container as **root**. Some share systems my limit this feature and only
allow running containers as a user. When the container is run as
**root**, files written out to filesystems mounted from the host will
have the user id `1000` by default. In other words, you'll need to be
able to run as root in the host to change permissions or manage these
files. Alternatively, running as a user allows preempting these
permissions issues. It is possible to run as a user with the `-u`
argument. In general, we will want to use the same user ID as the
running user in the host to ensure the ownership of files written during
the container execution. Therefore, you will generally run the container
with `-u $( id -u )`.

You may also invoke `docker` directly:

``` Shell
$ docker run -ti --rm \
    -v path/to/data:/data:ro \
    -v path/to/output:/out \
    poldracklab/fmriprep:<latest-version> \
    /data /out/out \
    participant
```

For example: :

```
$ docker run -ti --rm \
    -v $HOME/ds005:/data:ro \
    -v $HOME/ds005/derivatives:/out \
    -v $HOME/tmp/ds005-workdir:/work \
    poldracklab/fmriprep:<latest-version> \
    /data /out/fmriprep-<latest-version> \
    participant \
    -w /work
```

Once the Docker Engine arguments are written, the remainder of the
command line follows the [usage](https://fmriprep.readthedocs.io/en/latest/usage.html).
In other words, the first section of the command line is all equivalent to the
`fmriprep` executable in a *bare-metal* installation: :

``` Shell
$ docker run -ti --rm \                      # These lines
    -v $HOME/ds005:/data:ro \                # are equivalent to
    -v $HOME/ds005/derivatives:/out \        # a call to the App's
    -v $HOME/tmp/ds005-workdir:/work \       # entry-point.
    poldracklab/fmriprep:<latest-version> \  #
    \
    /data /out/fmriprep-<latest-version> \   # These lines correspond
    participant \                            # to the particular BIDS
    -w /work                                 # App arguments.
```