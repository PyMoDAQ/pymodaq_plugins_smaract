pymodaq_plugins_smaract (Smaract)
#################################




.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_smaract.svg
   :target: https://pypi.org/project/pymodaq_plugins_smaract/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_smaract/workflows/Upload%20Python%20Package/badge.svg
    :target: https://github.com/PyMoDAQ/pymodaq_plugins_smaract

PyMoDAQ plugin for actuators from Smaract (MCS_controller, ...)


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

* **MCS2** positioner with sensor (S option) with MCS2 controller
* **SmaractMCS** SLC linear stages with sensor (S option) with MCS controller
* **SmaractMCS2** SLC linear stages with sensor (S option) with MCS2 controller (Legacy, use the MCS2)
* **SmaractSCU** SLC linear or angular stages with or without sensors using the Instrumental-lib package and the
  simpler SCU controller


Installation instructions
=========================

Operating system: Windows 7 or 10 (Mac and linux for the **MCS2**)
Python: >=3.9
PyMoDAQ: >=5.0.2

The **MCS2** actuator uses python bindings of the Smaract Library as provided by Smaract.
It can seamlessly be used on any platform once you've installed the corresponding SDK (and its *.dll or *.so
library)



