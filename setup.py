import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="namebase-exchange", # Replace with your own username
    version="0.0.4",
    python_requires='>=3.6',
    author="Wing Chan",
    author_email="wingyungchan@gmail.com",
    description="Python Client to interact with the Namebase Exchange API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wy/namebase-exchange-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English'
    ]
)