from distutils.core import setup
setup(
name = 'titration_plot',
packages = ['titration_plot'],
version = '0.1.3',
license = 'gpl-3.0', 
description = 'Plotting for titration adapted from https://pypi.org/project/titration/',
author = 'Puck van Gerwen',
author_email = 'puck.vangerwen@gmail.com',
url = 'https://github.com/puckvg/titration_plot',
download_url = 'https://github.com/puckvg/titration_plot/archive/v_013.tar.gz', 
keywords = ['titration', 'pH'],
install_requires = ['scipy', 'matplotlib'],
classifiers = [
'Development Status :: 4 - Beta', 
'Intended Audience :: Developers',
'Topic :: Software Development :: Build Tools',
'Programming Language :: Python :: 3',
'Programming Language :: Python :: 3.4',
'Programming Language :: Python :: 3.5',
'Programming Language :: Python :: 3.6']
)


