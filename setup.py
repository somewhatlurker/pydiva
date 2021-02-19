import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydiva",
    version="1.1.0",
    author="somewhatlurker",
    description="Some stuff for handling files from Project DIVA games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/somewhatlurker/pydiva",
    packages=setuptools.find_packages(exclude=['tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
       'construct>=2.9.0',
       'pycryptodomex',
    ],
)