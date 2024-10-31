(archiving-overview)=
# Archiving

Archiving is a functionnality allowing to store attribute values.

Archiving in Tango started with HDB, which is deprecated, and is now called HDB++. 
SNAP allows to store attribute values as snapshots.

HDB++ supports higher time resolution, multiple database backends (MySQL, timescaledb, sqlite…), and is based on events.

HDB++ is designed to have a higher throughput and a number of improvements like better error management, lower footprint etc.

```{toctree}
hdbpp.md
snap.md
```

