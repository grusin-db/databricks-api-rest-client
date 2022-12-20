import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="databricks-cli-rest-client",
  version="0.0.1",
  author="Grzegorz Rusin",
  author_email="grzegorz.rusin@databricks.com",
  description="Simple databricks rest api client",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.9',
)