Django Loaddata Incremental
===========================

Ever had that problem, that you changed one tiny thing in your Django dummy data fixtures but had to reload your whole DB afterwards, because fixtures don't apply if there's already data in the DB? No? Well I do all the time.

This plugin adds a simple management.py task, namely `loaddata_incremental`, that - as the name suggests - loads fixtures just like the builtin command, but does so incrementaly.

For documentation on fixtures and the loaddata command itself you best consider the official django documentation for respective things.

This plugin only accepts JSON input (for now).

---

Installation is easy. Just add `loaddata_incremental` to you `INSTALLED_APPS` and you're done.
