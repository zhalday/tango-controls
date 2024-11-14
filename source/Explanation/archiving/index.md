(archiving-overview)=

# Archiving

(archiving)=

```{tags} audience:all, lang:all
```

The Archiving of Tango Controls allows one to store [Attribute](#attribute-explanation) values.

The current recommendation for archiving of Attribute values is to use the Historical Data Base++ or [HDB++](hdbpp-manual). HDB++ supports high time resolution, multiple database backends (MySQL, Timescale, SQLite), and is based on Tango Attribute [events](#events-tangoclient). The improvements over its now deprecated predecessor HDB are higher throughput and a number of improvements behind the curtain, among them better error handling and smaller demand for resources (RAM and CPU).

There is also [SNAP](#snap-archiving-tool). It is not a real archiver in the way that HDB++ works, but it allows to take snapshots of sets of attributes at the same time[^same_time]. One can think of it as a camera that can only take photos of one moment in time but not videos. HDB++ on the other hand could be configured to act almost like a video recorder if one had unlimited resources (RAM, CPU, storage space).

[^same_time]: _Same time_ is not really possible because a distributed control system will always introduce delays somewhere. What we refer to here is a best effort: The computer that takes the snapshot will read the values of all attribute as fast as possible. It is possible that a device does not reply immediately when one of its attributes is read. This will result in a delay that one will notice when looking at the timestamps of the attributes in the snapshot.

```{toctree}
hdbpp.md
snap.md
```
