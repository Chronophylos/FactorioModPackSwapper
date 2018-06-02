======================
FactorioModPackSwapper
======================
Simple Modpack Swapper for Factorio
-----------------------------------

Configuration
-------------

The config is a YAML file called ``fmps.yml``.
Top level keys are:

* ``symlink``: ``true`` or ``false``; either user symlinks or copy the mods directly
* ``config``: your factorio config path where the ``mods`` folder is
* ``modpacks``: a list of modpacks descibed below
Modpack keys:

* The key itself is the name of the mod
* ``directory``: a subdirectory of ``config/modpacks`` with your mods
* ``symlink``: see above

An example below

.. code:: yaml

  symlink: false #  create a symlink instead of copying the mods # default: true
  config: '%appdata%/Factorio' # example on windows
  modpacks:
    SeaBlock 0.27 Chrono: #  modpack name
      directory: seablock_0.27-chrono #  directory where your mods reside
    Vanilla:
      directory: vanilla
    OmegaPack 0.1.0:
      directory: omegapack_0.1.0

Usage
-----

Just start the binary after setting up the config
