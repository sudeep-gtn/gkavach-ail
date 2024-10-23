AIL
===

<p align="center">
<img src="https://raw.githubusercontent.com/ail-project/ail-framework/master/var/www/static/image/ail-icon.png" height="250" />
</p>

<table>
<tr>
  <td>Latest Release</td>
  <td><a href="https://github.com/ail-project/ail-framework/releases/latest"><img src="https://img.shields.io/github/release/ail-project/ail-framework/all.svg"></a></td>
</tr>
<tr>
  <td>CI</td>
  <td><a href="https://github.com/CIRCL/AIL-framework/actions/workflows/ail_framework_test.yml"><img src="https://github.com/CIRCL/AIL-framework/actions/workflows/ail_framework_test.yml/badge.svg"></a></td>
</tr>
<tr>
  <td>Gitter</td>
  <td><a href="https://gitter.im/ail-project/?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge"><img src="https://badges.gitter.im/ail-project.svg" /></a></td>
</tr>
<tr>
  <td>Contributors</td>
  <td><img src="https://img.shields.io/github/contributors/ail-project/ail-framework.svg" /></td>
</tr>
<tr>
  <td>License</td>
  <td><img src="https://img.shields.io/github/license/ail-project/ail-framework.svg" /></td>
</tr>
</table>

![Logo](./doc/logo/logo-small.png?raw=true "AIL logo")

AIL framework - Framework for Analysis of Information Leaks

AIL is a modular framework to analyse potential information leaks from unstructured data sources like pastes from Pastebin or similar services or unstructured data streams. AIL framework is flexible and can be extended to support other functionalities to mine or process sensitive information (e.g. data leak prevention).

![Dashboard](./doc/screenshots/dashboard.png?raw=true "AIL framework dashboard")


![Finding webshells with AIL](./doc/screenshots/webshells.gif?raw=true "Finding websheels with AIL")

Features
--------

* Modular architecture to handle streams of unstructured or structured information
* Default support for external ZMQ feeds, such as provided by CIRCL or other providers
* Multiple feed support
* Each module can process and reprocess the information already processed by AIL
* Detecting and extracting URLs including their geographical location (e.g. IP address location)
* Extracting and validating potential leaks of credit card numbers, credentials, ...
* Extracting and validating leaked email addresses, including DNS MX validation
* Module for extracting Tor .onion addresses (to be further processed for analysis)
* Keep tracks of duplicates (and diffing between each duplicate found)
* Extracting and validating potential hostnames (e.g. to feed Passive DNS systems)
* A full-text indexer module to index unstructured information
* Statistics on modules and web
* Real-time modules manager in terminal
* Global sentiment analysis for each providers based on nltk vader module
* Terms, Set of terms and Regex tracking and occurrence
* Many more modules for extracting phone numbers, credentials and others
* Alerting to [MISP](https://github.com/MISP/MISP) to share found leaks within a threat intelligence platform using [MISP standard](https://www.misp-project.org/objects.html#_ail_leak)
* Detect and decode encoded file (Base64, hex encoded or your own decoding scheme) and store files
* Detect Amazon AWS and Google API keys
* Detect Bitcoin address and Bitcoin private keys
* Detect private keys, certificate, keys (including SSH, OpenVPN)
* Detect IBAN bank accounts
* Tagging system with [MISP Galaxy](https://github.com/MISP/misp-galaxy) and [MISP Taxonomies](https://github.com/MISP/misp-taxonomies) tags
* UI paste submission
* Create events on [MISP](https://github.com/MISP/MISP) and cases on [The Hive](https://github.com/TheHive-Project/TheHive)
* Automatic paste export at detection on [MISP](https://github.com/MISP/MISP) (events) and [The Hive](https://github.com/TheHive-Project/TheHive) (alerts) on selected tags
* Extracted and decoded files can be searched by date range, type of file (mime-type) and encoding discovered
* Graph relationships between decoded file (hashes), similar PGP UIDs and addresses of cryptocurrencies
* Tor hidden services crawler to crawl and parse output
* Tor onion availability is monitored to detect up and down of hidden services
* Browser hidden services are screenshot and integrated in the analysed output including a blurring screenshot interface (to avoid "burning the eyes" of the security analysis with specific content)
* Tor hidden services is part of the standard framework, all the AIL modules are available to the crawled hidden services
* Generic web crawler to trigger crawling on demand or at regular interval URL or Tor hidden services


Installation
------------

Type these command lines for a fully automated installation and start AIL framework:
```bash
# Clone the repo first
git clone https://github.com/ail-project/ail-framework.git
cd ail-framework

# For Debian and Ubuntu based distributions
./installing_deps.sh

# For Centos based distributions (Tested: Centos 8)
chmod u+x centos_installing_deps.sh
./centos_installing_deps.sh

# Launch ail
cd ~/ail-framework/
cd bin/
./LAUNCH.sh -l
```

The default [installing_deps.sh](./installing_deps.sh) is for Debian and Ubuntu based distributions.

There is also a [Travis file](.travis.yml) used for automating the installation that can be used to build and install AIL on other systems.

Requirement:
- Python 3.6+

Installation Notes
------------

In order to use AIL combined with **ZFS** or **unprivileged LXC** it's necessary to disable Direct I/O in `$AIL_HOME/configs/6382.conf` by changing the value of the directive `use_direct_io_for_flush_and_compaction` to `false`.

Tor installation instructions can be found in the [HOWTO](https://github.com/ail-project/ail-framework/blob/master/HOWTO.md#installationconfiguration)

Starting AIL
--------------------------

```bash
cd bin/
./LAUNCH.sh -l
```

Eventually you can browse the status of the AIL framework website at the following URL:

```
https://localhost:7000/
```

The default credentials for the web interface are located in ``DEFAULT_PASSWORD``. This file is removed when you change your password.

Training
--------

CIRCL organises training on how to use or extend the AIL framework. AIL training materials are available at [https://www.circl.lu/services/ail-training-materials/](https://www.circl.lu/services/ail-training-materials/).


API
-----

The API documentation is available in [doc/README.md](doc/README.md)

HOWTO
-----

HOWTO are available in [HOWTO.md](HOWTO.md)

Privacy and GDPR
----------------

[AIL information leaks analysis and the GDPR in the context of collection, analysis and sharing information leaks](https://www.circl.lu/assets/files/information-leaks-analysis-and-gdpr.pdf) document provides an overview how to use AIL in a lawfulness context especially in the scope of General Data Protection Regulation.

Research using AIL
------------------

If you write academic paper, relying or using AIL, it can be cited with the following BibTeX:

~~~~
@inproceedings{mokaddem2018ail,
  title={AIL-The design and implementation of an Analysis Information Leak framework},
  author={Mokaddem, Sami and Wagener, G{\'e}rard and Dulaunoy, Alexandre},
  booktitle={2018 IEEE International Conference on Big Data (Big Data)},
  pages={5049--5057},
  year={2018},
  organization={IEEE}
}
~~~~

Screenshots
===========


Tor hidden service crawler
--------------------------

![Tor hidden service](./doc/screenshots/ail-bitcoinmixer.png?raw=true "Tor hidden service crawler")

Trending charts
---------------

![Trending-Modules](./doc/screenshots/trending-module.png?raw=true "AIL framework modulestrending")

Extracted encoded files from pastes
-----------------------------------

![Extracted files from pastes](./doc/screenshots/ail-hashedfiles.png?raw=true "AIL extracted decoded files statistics")
![Relationships between extracted files from encoded file in unstructured data](./doc/screenshots/hashedfile-graph.png?raw=true "Relationships between extracted files from encoded file in unstructured data")

Browsing
--------

![Browse-Pastes](./doc/screenshots/browse-important.png?raw=true "AIL framework browseImportantPastes")

Tagging system
--------

![Tags](./doc/screenshots/tags.png?raw=true "AIL framework tags")

MISP and The Hive, automatic events and alerts creation
--------

![paste_submit](./doc/screenshots/tag_auto_export.png?raw=true "AIL framework MISP and Hive auto export")

Paste submission
--------

![paste_submit](./doc/screenshots/paste_submit.png?raw=true "AIL framework paste submission")

Sentiment analysis
------------------

![Sentiment](./doc/screenshots/sentiment.png?raw=true "AIL framework sentimentanalysis")

Terms tracker
---------------------------

![Term-tracker](./doc/screenshots/term-tracker.png?raw=true "AIL framework termManager")


[AIL framework screencast](https://www.youtube.com/watch?v=1_ZrZkRKmNo)

Command line module manager
---------------------------

![Module-Manager](./doc/screenshots/module_information.png?raw=true "AIL framework ModuleInformationV2.py")

License
=======

```
    Copyright (C) 2014 Jules Debra
    Copyright (C) 2014-2021 CIRCL - Computer Incident Response Center Luxembourg (c/o smile, security made in Lëtzebuerg, Groupement d'Intérêt Economique)
    Copyright (c) 2014-2021 Raphaël Vinot
    Copyright (c) 2014-2021 Alexandre Dulaunoy
    Copyright (c) 2016-2021 Sami Mokaddem
    Copyright (c) 2018-2021 Thirion Aurélien
    Copyright (c) 2021 Olivier Sagit

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
