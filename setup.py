from setuptools import setup, find_packages

setup(
    name="conda-diff",
    version="0.1.1dev1",
    author="Dominik Kutra",
    license="MIT",
    description="Command line tool to compare conda environments",
    # long_description=description,
    # url='https://...',
    package_dir={"": "src"},
    packages=find_packages("./src"),
    include_package_data=True,
    install_requires=["networkx", "sh"],
    entry_points={"console_scripts": ["conda-diff = conda_diff.cli:main"]},
)
