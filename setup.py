import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

short_description = long_description.split("\n")[2]

with open("requirements/prod.txt") as fh:
    install_requires = [lib for lib in fh.read().split("\n") if "==" in lib]

setuptools.setup(
    name="boar",
    version="0.0.0",
    author="Alexandre Cameron",
    author_email="lexcam@hotmail.fr",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
)
