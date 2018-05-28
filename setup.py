from distutils.core import setup
long_description = open('README.md').read()
VERSION = '0.1'

setup(
    name='autocomplete',
    version=VERSION,
    packages=['autocomplete',
              ],
    description='py3 and jieba version for autocomplete-redis.',
    long_description=long_description,
    author='LISHITING',
    author_email='leocatch@yeah.net',
    license='MIT License',
    url='https://github.com/LISHITING/autocomplete-redis-py3.git',
    platforms=["any"],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ], requires=['jieba', 'simplejson', 'redis']
)
