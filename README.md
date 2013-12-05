WheelCMS Valve
==============

![Build status](https://travis-ci.org/wheelcms/wheelcms_valve.png)
![Coverage](https://coveralls.io/repos/wheelcms/wheelcms_valve/badge.png?branch=master)

This package provides a fully functional Blog for the WheelCMS content
management system. It provides the necessary contetn types and integrates
whith WheelCMS's commenting system, workflow, and so on.

Installation
------------

Add wheelcms_comments to your INSTALLED_APPS *before* the wheelcms_axle package, e.g.

    INSTALLED_APPS = (
        "wheelcms_valve",
          ...
        "wheelcms_axle",
    )


if your base definition of INSTALLED_APPS is out of your direct control
(e.g. when using
[wheelcms_project](https://github.com/wheelcms/wheelcms_project)), try
something like this:

    INSTALLED_APPS = (
        "wheelcms_valve",
    ) + INSTALLED_APPS

You should now be able to create a "Valve Blog" with "Valve Entries" in your
site.
