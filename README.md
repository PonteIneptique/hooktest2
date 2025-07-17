![Header for HookTest](images/header.png)

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0) 
[![Software Test](https://github.com/cllg-project/hooktest/actions/workflows/test.yml/badge.svg)](https://github.com/cllg-project/hooktest/actions/workflows/test.yml)

Dapytains provides a server-side or client-side library to deal with
[Distributed Text Services APIs](https://distributed-text-services.github.io/) as well as
TEI XML files using the [CiteStructure](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-citeStructure.html)
encoding of their machine actionable architecture, allowing to split and retrieve reference in a file
"without human intervention".

HookTestv2, which replaces the original [HookTest](https://hal.science/hal-01709868/), allows for testing those file,
including tests for catalog registry.

**This software is still quite in alpha mode, feel free to report bugs**

## How to install

```sh
git clone https://github.com/cllg-project/hooktest.git
cd hooktest
python3 setup.py install
```

## How to run

If you want to test a system where you have a root catalog file, you can run `hooktest path/to/your/catalog.xml`
where catalog are using [`hooktest/resources/collection-schema.rng`](hooktest/resources/collection-schema.rng).

Otherwise, run `hooktest --no-catalog /path/to/your/tei/files.xml`.


## Support

Funded via the CLLG Project.

Ce travail a bénéficié d’une aide de l’État gérée par l’Agence Nationale de la
Recherche au titre de France 2030 portant la référence « ANR-24-RRII- 0002 » et opéré par
le Programme Inria Quadrant.