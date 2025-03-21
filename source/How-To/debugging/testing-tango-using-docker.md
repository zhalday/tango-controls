(tango-using-docker)=

# Using Tango docker containers

```{tags} audience:developers, lang:all
```

In this section we describe how one can test newly developed tango device server using [docker](https://www.docker.com/) containers.

Tango docker containers provide a lightweight solution for deploying tango, especially useful for local workstation development.

To get info on how to install docker on your machine please refer to the docker [documentation](https://docs.docker.com/engine/installation/).

Once docker is installed one can pull docker images with pre-installed tango.

## Tango docker containers

[SKAO] provides several docker containers for Tango development and deployment, including but not limited to:

> - ska-tango-images-tango-db: a (mysql-compatible) mariadb container with the Tango schema
> - ska-tango-images-tango-cpp: a container with core Tango libraries and dependencies that can run the `DatabaseDS` Device Server
> - ska-tango-images-rest-server: a [Tango REST server](https://gitlab.com/tango-controls/rest-server)
> - ska-tango-images-tango-test: the well-established [TangoTest device server](https://gitlab.com/tango-controls/TangoTest)

The sources for these docker images are hosted and maintained on the SKAO gitlab: <https://gitlab.com/ska-telescope/ska-tango-images>

These container images are hosted on [SKAO] artefact repository: <https://artefact.skao.int>. At the moment they cannot be browsed for via the
repository website, however, it is possible to search for images at the [SKAO] 

-These container images are hosted on [SKAO] Harbor service: <https://harbor.skao.int/>. At the moment they cannot be browsed and one has to search for them. Just enter ska-tango-image in the search box and Harbor will list all images that SKAO provides. The images can must be pulled with the prefix `artefact.skao.int/`.  [SKAO] also provide a catalogue of images which can be viewed here: <https://developer.skao.int/projects/ska-tango-images/en/stable/>.  This catalogue contains basic usage instructions for each image.

### Tango docker stack

The easiest way to setup the whole stack on a local development/test computer is to use [docker compose](https://docs.docker.com/compose/).  The [SKAO] provides How-To guides for spinning up different Tango configurations using docker compose.

For example, [this guide](https://developer.skao.int/projects/ska-tango-images/en/stable/how-to/rest-with-docker-compose.html) describes how to start a Tango database and Tango RestServer using the images provided by [SKAO] and docker compose.

More guides are available [here](https://developer.skao.int/projects/ska-tango-images/en/stable/).

[skao]: https://developer.skao.int/en/latest/index.html
