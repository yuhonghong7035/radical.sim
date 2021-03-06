__author__    = "RADICAL Team"
__copyright__ = "Copyright 2014, RADICAL Research, Rutgers University"
__license__   = "MIT"


""" Setup script. Used by easy_install and pip. """

import os
import sys
import subprocess as sp

from setuptools import setup, find_packages, Command

name     = 'radical.sim'
mod_root = 'src/radical/sim/'

#-----------------------------------------------------------------------------
#
# versioning mechanism:
#
#   - version:          1.2.3            - is used for installation
#   - version_detail:  v1.2.3-9-g0684b06 - is used for debugging
#   - version is read from VERSION file in src root, which is on installation
#     copied into the module dir.
#   - version_detail is derived from the git tag, and only available when
#     installed from git -- this is stored in VERSION.git, in the same
#     locations, on install.
#   - both files, VERSION and VERSION.git are used to provide the runtime
#     version information.
#
def get_version (mod_root):
    """
    mod_root
        a VERSION and VERSION.git file containing the version strings is created
        in mod_root, during installation.  Those files are used at runtime to
        get the version information.

    """

    try:

        version        = None
        version_detail = None

        # get version from './VERSION'
        src_root = os.path.dirname (__file__)
        if  not src_root :
            src_root = '.'

        with open (src_root + "/VERSION", "r") as f :
            version = f.readline ().strip()


        # attempt to get version detail information from git
        p   = sp.Popen ('cd %s ; '\
                        'tag=`git describe --tags --always` ; '\
                        'branch=`git branch | grep -e "^*" | cut -f 2 -d " "` ; '\
                        'echo $tag@$branch'  % src_root,
                        stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
        version_detail = p.communicate()[0].strip()

        if  p.returncode   !=  0  or \
            version_detail == '@' or \
            'fatal'        in version_detail :
            version_detail =  "v%s" % version

        print 'version: %s (%s)'  % (version, version_detail)


        # make sure the version files exist for the runtime version inspection
        path = "%s/%s" % (src_root, mod_root)
        print 'creating %s/VERSION' % path

        with open (path + "/VERSION",     "w") as f : f.write (version        + "\n")
        with open (path + "/VERSION.git", "w") as f : f.write (version_detail + "\n")

        return version, version_detail

    except Exception as e :
        raise RuntimeError ("Could not extract/set version: %s" % e)


#-----------------------------------------------------------------------------
# get version info -- this will create VERSION and srcroot/VERSION
version, version_detail = get_version (mod_root)


#-----------------------------------------------------------------------------
# check python version. we need > 2.6, <3.x
if  sys.hexversion < 0x02060000 or sys.hexversion >= 0x03000000:
    raise RuntimeError("%s requires Python 2.x (2.6 or higher)" % name)


#-----------------------------------------------------------------------------
#
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


#-----------------------------------------------------------------------------
setup_args = {
    'name'             : name,
    'version'          : version,
    'description'      : "The RADICAL simulator framework",
    'long_description' : (read('README.md') + '\n\n' + read('CHANGES.md')),
    'author'           : 'RADICAL Group at Rutgers University',
    'author_email'     : "mark.santcroos@rutgers.edu",
    'maintainer'       : "Mark Santcroos",
    'maintainer_email' : "mark.santcroos@rutgers.edu",
    'url'              : "https://github.com/radical-cybertools/radical.pilot",
    'license'          : "MIT",
    'keywords'         : "radical simulator distributed computing",
    'classifiers'      : [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Distributed Computing',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix'
    ],

    'namespace_packages': ['radical'],
    'packages'    : find_packages('src'),
    'package_dir' : {'': 'src'},
    'scripts'          : ['bin/radicalsim-version'
                         ],
    'package_data'     : {'': ['*.sh', '*.json', 'VERSION', 'VERSION.git']},

    'install_requires' : ['setuptools', 'simpy', 'radical.utils'],
    'tests_require'    : ['setuptools', 'nose'],
    'test_suite'       : 'radical.sim.tests',
    'zip_safe'         : False,
}

#-----------------------------------------------------------------------------

setup (**setup_args)

#-----------------------------------------------------------------------------
