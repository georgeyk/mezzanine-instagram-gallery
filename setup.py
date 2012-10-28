# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2012 - George Y. Kussumoto <georgeyk.dev@gmail.com>
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##

from setuptools import setup, find_packages
import sys, os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import mezzanine_instagram_gallery

setup(
    name='mezzanine-instagram-gallery',
    version=mezzanine_instagram_gallery.VERSION,
    url=mezzanine_instagram_gallery.SITE,
    author=mezzanine_instagram_gallery.AUTHOR,
    author_email=mezzanine_instagram_gallery.EMAIL,
    license=mezzanine_instagram_gallery.LICENSE,
    description=u'Instagram image galleries in Mezzanine.',
    long_description=open('README.md').read(),
    keywords='django, mezzanine, instagram',
    packages=find_packages(),
    setup_requires=('setuptools'),
    install_requires=('setuptools', 'mezzanine>=1.2.4',
                      'python-instagram>=0.8.0', 'requests>=0.14.1',),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later '
                                                                  '(GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: '
                              'Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',],
    zip_safe=False,
    include_package_data=True,
)
