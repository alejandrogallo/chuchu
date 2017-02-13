from setuptools import setup

import chuchu


setup(
    name        = "chuchu",
    version     = chuchu.__version__,
    description = "A quantum chemistry utilities package",
    url         = "http://github.com/alejandrogallo/chuchu",
    author      = "Alejandro Gallo",
    license     = "MIT",
    packages    = ["chuchu"],
    test_suite  = "chuchu.tests",
    scripts     = [],
    zip_safe    = False
    )


