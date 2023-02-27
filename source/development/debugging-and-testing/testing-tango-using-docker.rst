.. _tango_using_docker:

Using Tango docker containers
=============================

:audience:`advanced developers`, :lang:`all`

In this section we describe how one can test newly developed tango device server using `docker <https://www.docker.com/>`_ containers.

Tango docker containers provide a lightweight solution for deploying tango.

To get info on how to install docker on your machine please refer to the docker `documentation <https://docs.docker.com/engine/installation/>`_.

Once docker is installed one can pull docker images with pre-installed tango.

Tango docker containers
-----------------------

`SKAO`_ provides several docker containers for Tango development and deployment, including but not limited to: 

 * tango-db: a (mysql-compatible) mariadb container with the Tango schema 
 * tango-cpp: a container with core Tango libraries and dependencies
 * tango-rest: a `Tango REST server <https://github.com/tango-controls/rest-server>`_
 * tango-test: the well-established `TangoTest device server <https://gitlab.com/tango-controls/TangoTest>`_

These container images are hosted on `SKAO`_ Nexus service: https://artefact.skao.int/#browse/browse:docker-all from where they can be pulled with the prefix ``artefact.skao.int/``

The sources for these docker images are hosted and maintained on the SKAO gitlab: https://gitlab.com/ska-telescope/ska-tango-images

.. _SKAO: https://developer.skao.int/en/latest/index.html


Tango docker stack
~~~~~~~~~~~~~~~~~~

Typical tango stack looks like this:

.. image:: testing-tango-using-docker/tango-stack.png

The easiest way to setup the whole stack on a local development/test computer is to use `docker compose <https://docs.docker.com/compose/>`_

Here is very small example of docker-compose.yml which runs up the DB and the Database Device Server:

.. code-block:: yaml

    version: '3'
    networks:
      tango-net:
        name: tango-net
        driver: bridge

    services:
      tango-db:
        image: artefact.skao.int/ska-tango-images-tango-db:10.4.19
        platform: linux/x86_64
        networks:
          - tango-net
        ports:
          - "9999:3306"
        environment:
          - MARIADB_ROOT_PASSWORD=root
          - MARIADB_DATABASE=tango
          - MARIADB_USER=tango
          - MARIADB_PASSWORD=tango

      tango-cs:
        image: artefact.skao.int/ska-tango-images-tango-cpp:9.3.13
        platform: linux/x86_64
        networks:
          - tango-net
        ports:
          - "10000:10000"
        environment:
          - TANGO_HOST=localhost:10000
          - MYSQL_HOST=tango-db:3306
          - MYSQL_USER=tango
          - MYSQL_PASSWORD=tango
          - MYSQL_DATABASE=tango
        links:
          - "tango-db:localhost"
        depends_on:
          - tango-db
        # Alternative to use health-check as a depends_on/condition
        # is to wait for port to be open:
        entrypoint:
          - /usr/local/bin/wait-for-it.sh
          - tango-db:3306 --timeout=30 --strict
          - --
          - /usr/local/bin/DataBaseds 2 -ORBendPoint giop:tcp::10000

To start the whole stack execute ``docker compose up`` in the same directory as the above docker-compose yaml file.

Once docker containers are up and running one can access mysql on localhost:9999 and the tango host on localhost:10000

For instance, one can start `jive`_ (assuming it is installed on the system).

.. _jive: https://gitlab.com/tango-controls/jive

Tango docker stack for Tango REST API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One can setup Tango docker stack for Tango REST API as well. `SKAO`_ provides a containerized build of the `Tango Rest Server <https://github.com/tango-controls/rest-server>`_.

The following :download:`compose.yaml <testing-tango-using-docker/compose.yaml>` compose.yaml assembles the whole stack:

.. literalinclude:: testing-tango-using-docker/compose.yaml
  :language: yaml

Note this is almost the same as the previous, except we have added tango-rest and tango-test containers. A few seconds after the stack has been started with ``docker compose up``, the Tango REST API can be accessed at http://localhost:8080/tango/rest/rc4/

The default username/password is ``tango-cs/tango`` and an example query from the host might look like this:

.. code-block:: shell

    curl -s -u "tango-cs:tango" http://localhost:8080/tango/rest/rc4/hosts/tango-cs/10000/devices/dserver/TangoTest/test/ | python3.11 -m json.tool
    {
        "name": "dserver/TangoTest/test",
        "info": {
            "last_exported": "24th February 2023 at 14:23:11",
            "last_unexported": "?",
            "name": "dserver/tangotest/test",
            "ior": "IOR:010000001700000049444c3a54616e676f2f4465766963655f353a312e3000000100000000000000ad000000010102000b0000003137322e32362e302e350000bbdd00000e000000fe4fc8f86300000001000000000100000300000000000000080000000100000000545441010000001c000000010000000100010001000000010001050901010001000000090101000254544141000000010000000d00000031393031363536316539356300000000250000002f746d702f6f6d6e692d74616e676f2f3030303030303030312d3136373732343835393100",
            "version": "5",
            "exported": true,
            "pid": 1,
            "server": "TangoTest/test",
            "hostname": "19016561e95c",
            "classname": "unknown",
            "is_taco": false
        },
        "attributes": "http://localhost:8080/tango/rest/rc4/hosts/tango-cs/10000/devices/dserver/TangoTest/test//attributes",
        "commands": "http://localhost:8080/tango/rest/rc4/hosts/tango-cs/10000/devices/dserver/TangoTest/test//commands",
        "pipes": "http://localhost:8080/tango/rest/rc4/hosts/tango-cs/10000/devices/dserver/TangoTest/test//pipes",
        "properties": "http://localhost:8080/tango/rest/rc4/hosts/tango-cs/10000/devices/dserver/TangoTest/test//properties",
        "state": "http://localhost:8080/tango/rest/rc4/hosts/tango-cs/10000/devices/dserver/TangoTest/test//state",
        "_links": {
            "_self": "http://localhost:8080/tango/rest/rc4/hosts/tango-cs/10000/devices/dserver/TangoTest/test/",
            "_parent": "http://localhost:8080/tango/rest/rc4/hosts/tango-cs/10000/devices/dserver/"
        }
    }
 


