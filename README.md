Finder Tags Butler
==================

>*Synchronize Mac OS Finder tags between several machines*

![Status](http://www.borja.glezseoane.es/img/project-status-label-development.svg "Status: development")  

The goal of this program is to synchronize **Mac OS Finder tags**, that are not automatically synchronized by OneDrive or similar services, between several Mac OS machines.


## How it works

The program uses a `.ftb` file to store metadata about the directory to get synced. The user has to select on or more *nodes*. A *node* is the root directory of a OneDrive or similar services directories. All the stuff under this *node* will be managed by the tool. Only one `.ftb` file will be created at this *node* directory.

The user is responsible for running the tool every time they make changes to the Finder tags or add these tasks to their automatic routines at the operating system level, as if it were launching a script.

Some use examples:

- To save a manifest:

```sh
ftbutler -s ~/OneDrive
```

- To dump a manifest:

```sh
ftbutler -d ~/OneDrive
```

See the context menu for more help.

```sh
ftbutler -h
```


## Install notes

The program is currently under development, but the first development versions can already be installed using Homebrew or PyPI. 


### Using Homebrew

```sh
brew install bglezseoane/tap/finder-tags-butler
```


### Using PyPI

First install [Tag](https://github.com/jdberry/tag) (e.g. with `brew install tag`). Then use:

```sh
pip install finder-tags-butler
```
