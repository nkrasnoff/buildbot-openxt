# OpenXT Auto builder

## Configuration

Create the Buildbot master:

```sh
buildbot@master $ buildbot create-master -r <basedir>
buildbot@master $ git clone https://github.com/eric-ch/openxt-buildbot.git .
```

You will need to register your buildbot-workers by editing `master.cfg`:
```python
c['workers'] = [
    worker.Worker("worker-name", "password"),
]
```

This needs to match each worker configuration.
```sh
buildbot@worker $ buildbot-worker create-worker --umask=0o22 <basedir> <master-host>:9989 "worker-name" "password"
```

As well, the master needs some configuration, edit the main dictionaries for
various worker groups, e.g:
```python
workers_oe_10['names'] = [ 'debian10-0' ]
workers_oe_10['workdir'] = "/var/builds/openxt"
workers_oe_10['deploydir'] = "/srv/http/OpenXT/auto"

workers_win_10['names'] = ["OpenXT-Win-0"]
workers_win_10['workdir'] = "c:\\builds"
workers_win_10['deploydir'] = "/srv/http/OpenXT/auto/windows"
```
Note: This uses rsync/scp to copy the built artefacts with `urlhost:urlpath` as
destination.


Create at least an admin user for the Buildbot interface:
```sh
buildbot@master $ ls buildbot.tac master.cfg
buildbot.tac  master.cfg
buildbot@master $ htpasswd -c .htpasswd user passwd
```

Start the master:
```sh
root@master $ systemctl start buildbot@<basedir>.service
```

Depending on your setup, allow TCP traffic to port 8010 (Buildbot HTTP UI) and
9989 (Buildbot Worker registration service). The following example should be
narrowed down depending on your network structure (filter local IPs and what
not).

```sh
root@master # iptables -A INPUT -p tcp -m tcp --dport 8010
root@master # iptables -A INPUT -p tcp -m tcp --dport 9989
```

## Before building, on the workers:

Deploy your certificates.
Using the default path: `/var/builds/openxt/certs` will be where the `.pem`
files should be found.
Example with a self signed certificate:
```sh
buildbot@worker $ cd /var/builds/openxt
buildbot@worker $ mkdir certs
buildbot@worker $ openssl genrsa -out certs/prod-cakey.pem 2048
buildbot@worker $ openssl genrsa -out certs/dev-cakey.pem 2048
buildbot@worker $ openssl req -new -x509 -key certs/prod-cakey.pem -out certs/prod-cacert.pem -days 1095
buildbot@worker $ openssl req -new -x509 -key certs/dev-cakey.pem -out certs/dev-cacert.pem -days 1095
```

## Sources

The OpenXT Auto-Builder is split in different files:
- `config_*.py` with the default repository configurations for various builds.
- `config.py` with helpers to aggregate these for Buildbot consumption.
- `schedulers.py` holds the schedulers definition, including forced interfaces.
- `factories_openxt.py` has the builders factories definitions for the OE
  components.
- `factories_wintools.py` has the builders factories definitions for Windows
  components.

## Improvements

- Push the certificate to the worker from the build-master.
- `repo_quick` should be fixed, see inline comments.
- Replace Buildbot Upload steps with Rsync
 * Easier/Safer to manage `authorized_keys` with the hosting component
   fetching.
