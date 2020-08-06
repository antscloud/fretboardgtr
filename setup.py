import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fretboardgtr", # Replace with your own username
    version="0.0.4",
    author="Ant Gib",
    author_email="ant.gib@protonmail.com",
    description="This is a package for creating chords and fretboard visualisation of scale in svg format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antscloud/fretboardgtr/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    'cssselect2 >=0.3.0',
    'lxml>=4.5.1',
    'Pillow>=7.1.2',
    'reportlab>=3.5.42',
    'svglib>=1.0.0',
    'svgwrite>=1.4',
    'tinycss2>=1.0.2',
    'webencodings>=0.5.1'
      ],
    python_requires='>=3',
)
