from setuptools import setup, find_packages

setup(
    name="conda_diff",
    version="0.1.0dev1",
    author="Dominik Kutra",
    license="MIT",
    description="Command line tool to compare conda environments",
    # long_description=description,
    # url='https://...',
    package_dir={"": "src"},
    packages=find_packages("./src"),
    include_package_data=True,
    install_requires=[
        # 'dep1>=1.0,<2',
        # 'dep2>=2'
    ],
    entry_points={
        "console_scripts": ["conda_diff = conda_diff.__main__:main"]
    },
)
