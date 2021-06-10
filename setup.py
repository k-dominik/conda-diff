from setuptools import setup, find_packages

setup(
    name="conda-diff",
    version="0.2.0dev0",
    author="Dominik Kutra",
    license="MIT",
    license_files=("LICENSE",),
    description="Command line tool to compare conda environments",
    # long_description=description,
    # url='https://...',
    package_dir={"": "src"},
    packages=find_packages("./src"),
    include_package_data=True,
    install_requires=["networkx"],
    entry_points={"console_scripts": ["conda-diff = conda_diff.cli:main"]},
)
