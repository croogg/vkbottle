"""
 MIT License

 Copyright (c) 2019 Arseniy Timonik

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""

from vkbottle.portable import VERSION
import setuptools

from distutils.core import setup
setup(
  name='vkbottle',
  packages=['vkbottle'],
  version=VERSION,
  license='MIT',
  description='New bot-creating repo with options control like in the famous framework flask!',
  author='Arseniy Timonik',
  author_email='timonik.bss@gmail.com',
  url='https://github.com/timoniq/vkbottle',
  long_description=open('OLD-README.md', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  download_url='https://github.com/timoniq/vkbottle/archive/v' + VERSION + '.tar.gz',
  keywords=['vk', 'vkontakte', 'vk-api', 'vk-bot', 'vkbottle', 'vk-bottle'],
  install_requires=[
    'aiohttp'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)