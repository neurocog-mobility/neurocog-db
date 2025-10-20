# neurocog-db

Link to full documentation: https://neurocog-mobility.github.io/neurocog-db/

## Installation

Run the following from a terminal:

```
pip install git+https://github.com/neurocog-mobility/neurocog-db.git
```

## Configuration

To view the currently configured path to the NeuroCog Drive root folder, use:
```
neurocogdb config
```

To set a new path, use:
```
neurocogdb config --set
```
And enter the path into the prompt.

## Usage

Synchronize the backend data catalog using ```neurocogdb sync``` and launch the browser-based dashboard interface using ```neurcogdb gui```.