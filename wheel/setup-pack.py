#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Mani Jamali. GNU General Public License v3.0
#
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

import setuptools, os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyabr",  # Replace with your own username
    version="0.1.9",
    author="Mani Jamali",
    author_email="manijamali2003@gmail.com",
    description="Pyabr cloud software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manijamali2003/pyabr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    setup_requires=['wheel'],
    install_requires=[
        'PyQt5',
        'pyqtconsole',
        'py-cpuinfo',
        'requests',
        'gitpython'
    ],
    include_package_data=True,
)