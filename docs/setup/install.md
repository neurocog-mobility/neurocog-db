# Installation & Configuration

## NeuroCog DB

A Python 3+ installation is required to run NeuroCog DB. See Python installation instructions below if you do not have it installed on your current system.

It is recommended to install NeuroCog DB in a virtual environment in order to avoid package and versioning conflicts across Python libraries. See [Using virtual environments](./useful-info.md#using-virtual-environments) for more information.

To install NeuroCog DB:

1. [Open a terminal](./useful-info.md#using-the-terminal)  and run the installation command:

```
pip install git+https://github.com/neurocog-mobility/neurocog-db.git
```

2. Test the installation and view all available commands:

```
neurocogdb --help
```

### Upgrading NeuroCog DB

Once installed, to upgrade to a newer release add the ```--upgrade``` flag:

```
pip install --upgrade git+https://github.com/neurocog-mobility/neurocog-db.git
```

## Configuring NeuroCog DB

Neurocog DB requires setting a path to the root folder of the NeuroCog drive.
To view the currently configured path, run:

```
neurocogdb config
```

For a fresh installation, this should return ```None```.
To find the correct configuration path, [open a terminal](./useful-info.md#using-the-terminal) in the root folder of the NeuroCog drive on your computer.

To set the path, run:
```
neurocogdb config --set
```

Paste the folder path in the prompt and click *Ok*. You should get confirmation of the updated path.

## Syncing and viewing the data catalog

Once you have configured the root path, simply run:
```
neurocogdb sync
```

To update the data catalog, then run:
```
neurocogdb gui
```
Use *ctrl/command + click* on the URL displayed in the terminal to launch a browser-based interface to view the data catalog.

