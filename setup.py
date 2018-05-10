#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PostMail sendmail compatible MTA (Mail Transport Agent)
# Copyright (C)2014-2018 Takuya Sawada
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
# 
from setuptools import setup

setup(
	name = 'postmail',
	version='0.5.0',
	description='PostMail sendmail compatible MTA (Mail Transport Agent)',
	author='Takuya Sawada',
	author_email='takuya@tuntunkun.com',
	url='https://github.com/tuntunkun/postmail',
	license='Apache License 2.0',
	packages = ['postmail'],
	install_requires = [
	],
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Operating System :: POSIX',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Topic :: Communications :: Email',
		'Topic :: Communications :: Email :: Mail Transport Agents',
		'Topic :: Utilities'
	],
	entry_points = {
		'console_scripts': [
			'postmail=postmail:main'
		]
	}
)
