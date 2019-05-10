# Depx

![https://img.shields.io/pypi/v/depx.svg](https://pypi.python.org/pypi/depx)
![https://img.shields.io/travis/thermondo/depx.svg](https://travis-ci.org/thermondo/depx)


Examine and visualize dependencies used by Python modules.

This is a simple, exploratory prototype for now. The goal is to use explicit
`import` statements in a module to identify the names of its dependencies. This
will not always produce a complete picture of all other code a module uses,
since there is a multitude of ways to import or reference other code
dynamically. Idiomatic Django, for example, uses a number of them. Those are
all out of scope, however, although some might get considered at a later time.

In this early stage, all functionality, structure and interfaces are subject to
radical and surprising changes.


## Dev setup

All the dependencies you need for development are in `requirements-dev.txt`.

You can run tests by executing `$ pytest` in the project directory, or the
whole tox test suite by running `$ tox`.


## Envisioned use cases

The project should enable the following use cases, but might do so by handing
off the right kind of data to other software. If we do different things
ourselves, they should end up in different commands (or at least subcommands).

* visualize dependencies of module, package or project
* identify dependency cycles
* help identify unused dependencies


## Existing and potential functionality

Sketch of ideas. This is not meant as a plan, but to guide initial development.

### Find dependencies

- [x] identify all explicit imports a module makes
- [x] same for whole packages
- [ ] same for arbitrary directories
- [x] identify local imports (those are smelly)
- [ ] distinguish built-in, 3rd party and local dependencies


### Names

- [x] show fully qualified names for importing module and dependency
- [ ] ability to show only top-level names
- [ ] resolve relative imports to proper names
- [ ] resolve `*` imports


### Output formats

The identified dependencies are the edges of a directed graph. Output formats
should include several standard ways to consume such data.

- [x] JSON
- [x] GraphML
- [x] browser-ready HTML with visualization
- [ ] Graphviz (`.dot`)
- [ ] text with columns (to compose with Unix pipes)
