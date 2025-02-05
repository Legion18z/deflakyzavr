from setuptools import setup


def find_required() -> list[str]:
    with open("requirements.txt") as f:
        return f.read().splitlines()


def get_version(filename='deflakyzavr/version') -> str:
    return open(filename, "r").read().strip()


setup(
    name="deflakyzavr",
    version=get_version(),
    description="vedro.io plugin for creating ticket into jira for flaky duty",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andrey Maslov",
    author_email="legionus18z@gmail.com",
    python_requires=">=3.7",
    url="https://github.com/Legion18z/deflakyzavr",
    license="Apache-2.0",
    packages=['deflakyzavr'],
    scripts=['./scripts/deflakyzavr'],
    install_requires=find_required(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
    package_data={
        'deflakyzavr': ['version', 'py.typed'],
    },
)
