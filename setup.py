import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fretboardgtr", # Replace with your own username
    version="0.0.1",
    author="Ant Gib",
    author_email="ant.gib@protonmail.com",
    description="This is a package for creating chords and fretboard visualisation of scale in svg format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antscloud/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'svgwrite',
      ],
    python_requires='>=3',
)
