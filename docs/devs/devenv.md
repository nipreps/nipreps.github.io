
This document explains how to prepare a new development environment and update an existing environment, as necessary, for the development of *NiPreps*' components.
Some components may deviate from these guidelines, in such a case, please follow the guidelines provided in their documentation.

If you plan to contribute back to the community, making your code available via pull-request, please make sure to have read and understood the [Community Documents and Contributor Guidelines](../community/index.md).
If you plan to distribute derived code, please follow our [licensing guidelines](../community/licensing.md).

Development in Docker is encouraged, for the sake of consistency and portability.
By default, work should be built off of [`nipreps/fmriprep:unstable`](https://hub.docker.com/r/nipreps/fmriprep/), which tracks the `master` branch, or `nipreps/fmriprep:latest`, which tracks the latest release version (see [BIDS-Apps execution guide](../apps/docker.md) for the basic procedure for running).

It will be assumed the developer has a working repository in `$HOME/projects/fmriprep`, and examples are also given for [niworkflows](https://github.com/nipreps/niworkflows) and *NiPype*.

## Patching a working copy into a Docker container

In order to test new code without rebuilding the Docker image, it is possible to mount working repositories as source directories within the container.
The [Docker wrapper](../apps/docker.md#running-a-niprep-with-a-lightweight-wrapper) script simplifies this for the most common repositories:

```shell
    -f PATH, --patch-fmriprep PATH
                          working fmriprep repository (default: None)
    -n PATH, --patch-niworkflows PATH
                          working niworkflows repository (default: None)
    -p PATH, --patch-nipype PATH
                          working nipype repository (default: None)
```

For instance, if your repositories are contained in `$HOME/projects`:

```shell
$ fmriprep-docker -f $HOME/projects/fmriprep/fmriprep \
                  -n $HOME/projects/niworkflows/niworkflows \
                  -p $HOME/projects/nipype/nipype \
                  -i nipreps/fmriprep:latest \
                  $HOME/fullds005 $HOME/dockerout participant
```

Note the `-i` flag allows you to specify an image.

When invoking `docker` directly, the mount options must be specified
with the `-v` flag:

```shell
-v $HOME/projects/fmriprep/fmriprep:/usr/local/miniconda/lib/python3.7/site-packages/fmriprep:ro
-v $HOME/projects/niworkflows/niworkflows:/usr/local/miniconda/lib/python3.7/site-packages/niworkflows:ro
-v $HOME/projects/nipype/nipype:/usr/local/miniconda/lib/python3.7/site-packages/nipype:ro
```

For example,

```shell
$ docker run --rm -v $HOME/ds005:/data:ro -v $HOME/dockerout:/out \
    -v $HOME/projects/fmriprep/fmriprep:/usr/local/miniconda/lib/python3.7/site-packages/fmriprep:ro \
    nipreps/fmriprep:latest /data /out/out participant \
    -w /out/work/
```

In order to work directly in the container, pass the `--shell` flag to `fmriprep-docker`

```shell
$ fmriprep-docker --shell $HOME/ds005 $HOME/dockerout participant
```

This is the equivalent of using `--entrypoint=bash` and omitting the *fMRIPrep* arguments in a `docker` command:

```shell
$ docker run --rm -v $HOME/ds005:/data:ro -v $HOME/dockerout:/out \
    -v $HOME/projects/fmriprep/fmriprep:/usr/local/miniconda/lib/python3.7/site-packages/fmriprep:ro --entrypoint=bash \
    nipreps/fmriprep:latest
```

Patching containers can be achieved in Singularity analogous to `docker` using the `--bind` (`-B`) option:

```shell
$ singularity run \
    -B $HOME/projects/fmriprep/fmriprep:/usr/local/miniconda/lib/python3.7/site-packages/fmriprep \
    fmriprep.img \
    /scratch/dataset /scratch/out participant -w /out/work/
```

## Adding dependencies

New dependencies to be inserted into the Docker image will either be Python or non-Python dependencies.
Python dependencies may be added in three places, depending on whether the package is large or non-release versions are required.
The image [must be rebuilt](#rebuilding-docker-image) after any dependency changes.

Python dependencies should generally be included in the appropriate dependency metadata of the `setup.cfg` file found at the root of each repository.
If some the dependency must be a particular version (or set thereof), it is possible to use version filters in this `setup.cfg` file.

For large Python dependencies where there will be a benefit to pre-compiled binaries, [conda](https://github.com/conda/conda) packages may also be added to the `conda install` line in the [Dockerfile](https://github.com/nipreps/fmriprep/blob/29133e5e9f92aae4b23dd897f9733885a60be311/Dockerfile#L46).

Non-Python dependencies must also be installed in the Dockerfile, via a `RUN` command.
For example, installing an `apt` package may be done as follows:

```Dockerfile
RUN apt-get update && \
    apt-get install -y <PACKAGE>
```

## (Re)Building Docker image

If it is necessary to (re)build the Docker image, a local image named `fmriprep` may be built from within the local repository.
Let's assume it is located in `~/projects/fmriprep`:

```shell
~/projects/fmriprep$ VERSION=$( python get_version.py )
~/projects/fmriprep$ docker build -t fmriprep --build-arg VERSION=$VERSION .
```

The `VERSION` build argument is necessary to ensure that help text can be reliably generated.
The `get_version.py` tool constructs the version string from the current repository state.

To work in this image, replace `nipreps/fmriprep:latest` with just `fmriprep` in any of the above commands.
This image may be accessed by the [Docker wrapper](../apps/docker.md#running-a-niprep-with-a-lightweight-wrapper) via the `-i` flag, e.g.:

```shell
$ fmriprep-docker -i fmriprep --shell
```

## Code-Server Development Environment (Experimental)

To get the best of working with containers and having an interactive development environment, we have an experimental setup with [code-server](https://github.com/cdr/code-server).

!!! important

    We have [a video walking through the process](https://youtu.be/bkZ-NyUaTvg) if you want a visual guide.


**1. Build the Docker image**.
We will use the `Dockerfile_devel` file to build our development docker image:
```shell
$ cd $HOME/projects/fmriprep
$ docker build -t fmriprep_devel -f Dockerfile_devel .
```

**2. Run the Docker image**
We can start a docker container using the image we built (`fmriprep_devel`):
```shell
$ docker run -it -p 127.0.0.1:8445:8080 -v ${PWD}:/src/fmriprep fmriprep_devel:latest
```

!!! important "Windows Users"
    
    If you are using windows shell, `${PWD}` may not be defined, instead use the absolute path to your repository.

!!! important "Docker-Toolbox"

    If you are using Docker-Toolbox, you will need to change your virtualbox settings using [these steps as a guide](https://github.com/jdkent/tutDockerRstudio#additional-setup-for-docker-toolbox). For step 6, instead of `Name = rstudio; Host Port = 8787; Guest Port = 8787`, have `Name = code-server; Host Port = 8443; Guest Port = 8080`. Then in the docker command above, change `127.0.0.1:8445:8080` to `192.168.99.100:8445:8080`.

If the container started correctly, you should see the following on your console:

```shell
INFO  Server listening on http://localhost:8080
INFO    - No authentication
INFO    - Not serving HTTPS
```

Now you can switch to your favorite browser and go to: `http://127.0.0.1:8445` (or `http://192.168.99.100:8445` for Docker Toolbox).

**3. Copy `fmriprep.egg-info` into your `fmriprep/` project directory**
`fmriprep.egg-info` makes the package executable inside the docker container.
Open a terminal in vscode and type the following:

```shell
$ cp -R /src/fmriprep.egg-info /src/fmriprep/
```

### Code-Server Development Environment Features
- The editor is [vscode](https://code.visualstudio.com/docs)

- There are several preconfigured debugging tests under the debugging icon in the activity bar
  - see [vscode debugging python](https://code.visualstudio.com/docs/python/debugging) for details.

- The `gitlens` and `python` extensions are preinstalled to improve the development experience in vscode.
