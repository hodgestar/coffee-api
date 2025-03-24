from setuptools import setup, find_packages

setup(
    name="coffee-api",
    version="0.1.0a",
    url='http://github.com/hodgestar/coffee-api',
    license='BSD',
    description="Super-silly virtual coffee maker",
    long_description=open('README.rst', 'r').read(),
    author='Simon Cross',
    author_email='hodgestar@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.3.2',
        'gunicorn==23.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python:: 3',
    ],
)
