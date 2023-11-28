SmarAct plugin
##############


.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_smaract.svg
   :target: https://pypi.org/project/pymodaq_plugins_smaract/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_smaract/workflows/Upload%20Python%20Package/badge.svg
    :target: https://github.com/PyMoDAQ/pymodaq_plugins_smaract

PyMoDAQ plugin for actuators from Smaract (MCS and MCS2 controllers).

Documentation: http://pymodaq.cnrs.fr/

Authors
=======

* David Bresteau (david.bresteau@cea.fr)
* Sebastien J. Weber (sebastien.weber@cnrs.fr)

Instruments
===========
Below is the list of instruments included in this plugin

Actuators
+++++++++

* **SmarActMCS** SLC linear stages with sensor (S option) with MCS controller.
* **SmarActMCS_OpenLoop** Any stage in open loop operation with MCS controller.
* **SmarActMCS2** SLC linear stages with sensor (S option) with MCS2 controller.
* **SmarAct** SLC linear or angular stages with or without sensors using the Instrumental-lib package.


System requirements
===================

Operating system: Windows 7 or 10

The SmarAct drivers that are provided by the manufacturer should be installed. One should first test that the actuator
is moving with the GUI from SmarAct before using this plugin.
