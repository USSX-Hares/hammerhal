# Hammerhal datasheet compiler tool
Allows to generate hero cards and adversary datasheets and to compile them into .png images.

## I. Installation
1. Download python3 from the official site: https://www.python.org/downloads/
2. Open a console terminal as in the tartget directory, and execute command:
`python -m pip install -e .`

**Notes:**
 - python should be 3.5+. Could be checked by executing `python --version` and `python -m pip --version`
 - For Windows: you should run _cmd.exe_ as an administrator
 - For *nix: you should run this with the `sudo -H` command

## II. Creating a data source:
1. Go to the _'raw'_ submodule.
2. Copy a .json file from a directory of required type and edit it by analog. If you dare, you can see appropriate [JSON Schema](http://json-schema.org/) from _'schemas'_ directory of project root.
3. You will be notified during the compilation if your input is invalid.

## III. Run compiler
 - Compile ALL available raw. Could take a while:
```python compile.py all```
 - Compile specific Hero:
```python compile.py hero my hero name```
 - Compile specific Adversary:
```python compile.py adversary epic-adversary-group```
 - Compile all skills from the original _Shadow over Hammerhal_ set (requires appropriate template):
```python compile.py card set:hammerhal type:skill all```
 - Run in interactive mode, where all commands from above can be used from terminal:
```python compile.py interactive```

Compiled files are stored in the output directory. By default, all output files are scaled to 720px width. You can change this setting in configs/


## DEVELOPER WARNING:
It IS guaranteed that this tool IS working with correct installation, configuration and data. It is your responsibility for correctness of installation, reconfiguration and all data sources program is receiving.
If any questions and/or suggestions take place, you can contact me via the [vk.com](vk.com/zaitcev_pter) or [email](ussx.hares@yandex.ru)
