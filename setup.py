import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="toes", # Replace with your own username
    version="0.0.24",
    author="Sarah Gebauer",
    author_email="sarah@sarahgebauer.com",
    description="Toe template engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xgebi/Toes",
    package_dir={'toes': 'src'},
    packages=['toes'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Hippocratic License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)