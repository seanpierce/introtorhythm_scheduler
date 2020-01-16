# Scheduler

This project is a sub app of introtorhythm.com used to manage scheduled show processes on the web server.

## Primary operations

* Scheduled task runs on the Ubuntu server at the top of every hour.
* The task runs a script in the scheduler application.
  * The script in the scheduler application calls into the scheduler API to collect information regarding a currently scheduled show.
  * The script takes that information and kills any current ezstream processes and deletes any existing configuration files.
  * The script will generate new configuration files programmatically, then start a new ezstream process.

## Local development and testing

Testing locally requires that your machine has `icecast` and `ezstream` installed.

```shell
# mac osx
brew install icecast
brew install ezstream

# linux/ ubuntu
apt-get install icecast
apy-get install ezstream
```

The local icecast.xml config file on mac osx is installed at `/usr/local/etc/icecast.xml`. On linux/ ubuntu, it is located at `/etc/icecast/icecast.xml`.

To run icecast and ezstream:
```shell
icecast -c /path/to/icecast.xml
ezstream -c /path/to/ezstream.xml
```

In order for ezstream to have a mountable point-of-access on your local icecast installation, ensure that you add the proper config element to the icecast.xml file.

```xml
<!-- Normal mounts -->
<mount type="normal">
    <mount-name>/scheduler</mount-name>
    <stream-name>My Stream Name</stream-name>
    <stream-description>My Stream is an internet radio station.</stream-description>
    <stream-url>https://mystream.com/scheduler</stream-url>
    <type>application/mp3</type>
    <subtype>mp3</subtype>
    <burst-size>65536</burst-size>
    <mp3-metadata-interval>4096</mp3-metadata-interval>
</mount>
```