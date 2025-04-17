% level: advanced

% target: Tango client developer; DevOps

(tango-rest-api)=

# Tango REST API

```{tags} audience:developers, lang:all
```

:::{warning}
**The Tango REST API is in life support mode.**

The Tango collaboration will not make any improvements or fix bugs. If you are interested in becoming its maintainer, please get in touch with us on our mailing list, in our forum, or at our bi-weekly Tango kernel meetings.
:::

Tango provides a REST API implementation. It can be used to integrate Tango with 3rd party products using the http protocol instead of the Tango protocol. A simple example could be a mobile client application for monitoring Tango.

This section addresses:

- What is REST and why it is useful?
- Getting started with simple example
- Example of a safe REST API deployment at ESRF
- Further steps

## Tango REST API specification

In short a REST API exports resources. These resources are accessible using URL addresses. Clients can then perform actions on these resources using a set of http methods. Typically these are:

- `GET` - request a resource
- `PUT` - update a resource
- `POST` - create a new resource
- `DELETE` - remove a resource

The Tango REST API exports Tango hosts; Tango devices; Tango device attributes, commands and pipes. So it follows [Tango Device Server Model](#device-server).

For example, one can request {term}`Tango Host` using Tango REST API:

```
GET tango/rest/rc4/hosts/tango_host/10000
```

Here one uses the Tango REST API implementation related to version [RC4](https://gitlab.com/tango-controls/rest-api/-/tree/rc4?ref_type=heads) as indicated by the
`tango/rest/rc4` part of the example URL. The `hosts` part will export the {term}`Tango Host` accessible through
this Tango REST API implementation and the `tango_host/10000` assumes that the `TANGO_HOST` address is set to `tango_host:10000`.

In the following example a client makes a request for a device attribute:

```
GET tango/rest/rc4/hosts/tango_host/10000/devices/sys/tg_test/1/attributes/double_scalar/value
```

Again here `tango/rest/rc4` relates to Tango REST API version RC4 implementation; `hosts/tango_host/10000` relates to `TANGO_HOST=tango_host:10000`; the `devices/sys/tg_test/1` relates to the device `tango://tango_host:10000/sys/tg_test/1` exported through the Tango REST API and finally `attributes/double_scalar/value` relates to the value of the attribute.

This third example shows how a client can execute a command on a device:

```
PUT tango/rest/rc4/hosts/tango_host/10000/devices/sys/tg_test/1/commands/DevDouble?v=3.14
```

Here the client executes `tango://tango_host:10000/sys/tg_test/1/DevDouble` with the input `arg=3.14`.


## Tango REST API implementations

Since the Tango REST API itself is only a specification one needs an actual implementation running somewhere.

Known implementations are listed in the Tango REST API [readme](https://gitlab.com/tango-controls/rest-api#known-server-implementations).

Please refer to the corresponding implementation documentation on how to install and use it.

In a nutshell download the latest fat jar distribution and start the server via `java -DTANGO_HOST=localhost:10000 -jar mtangorest.server.jar -nodb -dlist sys/rest/0`/

One can test the installation by attempting to read an attribute value from a device. Typically there is a `TangoTest` server running on the Tango host, whihc can be accesses through a browser at:

```
http://localhost:10001/tango/rest/rc4/hosts/localhost/10000/devices/sys/tg_test/1/attributes/double_scalar/value
```

showing:

```json
{
    "name":"double_scalar",
    "value":179.04696279859678,
    "quality":"ATTR_VALID",
    "timestamp":1493918496122
}
```

## Deployment

As Tango REST exports Tango via http to the internet the usual question is how to protect Tango from the unwanted activity?

The deployment of the Tango REST API can be made quite safe. Usually one wants to put the Tango REST API server behind a reverse proxy and restrict its access to a single {term}`Tango Host`. A reverse proxy can also allow connections only via https.

As every request via REST API must be validated against {term}`Tango Access Control` this adds an extra layer of security.

Below is a deployment scheme of REST API at ESRF. In this installation the REST API exports readonly forwarded attributes and is accessible via a secured http connection.

```{image} rest-api/ESRF.png
```

Every request passes through [HAProxy]<https://www.haproxy.org/> configured to use the https protocol for a secure connection. On its backend HAproxy communicates with the Tango REST server, which in turn can access only the Tango host where a device of class [ForwardComposer](https://gitlab.com/tango-controls/ForwardedComposer) is defined. This device provides read only access to the `MStatus` Tango device with status information about the storage ring at ESRF.

In addition the Tango REST API can be integrated with authentication and authorisation services like [Kerberos]<https://web.mit.edu/kerberos/#what_is>.

Finally, the Tango REST API implementation should use Tango Access Control to validate every request made from the internet.

## Further steps

- Install Tango REST API server locally or using docker.
- Develop your REST client or use a 3rd party framework.
- Deploy everything on the local network or in the cloud.

## References
\[1\] [Tango REST API specification on GitLab](https://gitlab.com/tango-controls/rest-api)
