# Useful Information

## Using the Terminal

A terminal is a text-based interface that lets you communicate with a computer's operating system.
It's also known as a command-line interface (CLI).

To launch a terminal on Windows, enter "Terminal" into the program search bar.
Closing the terminal window will also stop any processes currently running in the terminal.

To open a terminal in a specific folder, you can:

* **Option A:**
    Use the command: ``cd <path_to_folder>``

    Where you can replace ``<path_to_folder>`` with the folder path you would like to execute terminal commands in.

* **Option B:**
    Open the folder using File Explorer, then right-click in the folder and select **Open in Terminal**.


When copying/pasting text into the terminal, you can use the keyboard shortcuts
``Ctrl + Shift + C`` / ``Ctrl + Shift + V`` for copy/paste, respectively.


## Checking Python version

You can check which version of Python is installed by opening a [Terminal](#using-the-terminal) and entering
the command ``python -V``.

!!! note "Important"

    Some systems may use ``python3`` instead of ``python``. If you get a message ``Command 'python' not found.``
    then try again using: ``python3 -V``.

## Using virtual environments

Creating and using a virtual environment in Python is a crucial step for managing project dependencies. It ensures that each project has its own isolated set of packages, preventing conflicts between different projects.

1. **Create**: First, navigate to your project's root directory in your terminal. We'll name the virtual environment folder ```.venv``` (this is a common convention).

    ```
    python -m venv .venv
    ```

2. **Activate**: Before installing any packages for your project, you must activate the virtual environment. Activation changes your terminal's shell so that the ```python``` command points to the version inside the ```.venv``` folder, and ```pip``` installs packages there.

    * Windows (Powershell): ```.\.venv\Scripts\Activate.ps1```
    * Windows (Command Prompt): ```.\.venv\Scripts\activate.bat```
    * Mac/Linux: ```source .venv/bin/activate```

Once activated, your terminal prompt will usually be prefixed with the name of the environment (e.g., (.venv)):
```
(.venv) $
```
