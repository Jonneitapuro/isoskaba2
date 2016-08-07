# ISOskaba 2.0

An applet to track tutor activity in AYY. This is complete rewrite of this project. The old version is included as a submodule.

## Installation

- Requirements: 
  * Python 3.4.x [download it](https://www.python.org/downloads/release/python-340/)
  * virtualenv `sudo pip3 install virtualenv`
1. Install dependencies by running `./envinstall.sh`
2. Migrate Django `python3 manage.py migrate`
3. Start a locally served development server (localhost:8000) by running `python3 manage.py runserver`
4. There is also an script to automate virtualenv-schenanigans, called `test_applet.sh`


### About the project

Information about the project has been documented to the [wiki.](https://github.com/Jonneitapuro/isoskaba2/wiki)
