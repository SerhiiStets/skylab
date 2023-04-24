# Contributing to skylab


## Installation

1. Clone the project.

```
$ git clone git@github.com:SerhiiStets/skylab.git
```

2. Set up a virtual environment. The project is built and configured using poetry, but feel free to choose any virtual environment you prefer.

For poetry:

```
$ poetry install
$ poetry shell
```

3. Install the project in editable mode:

```
$ pip install -e .
```

4. Run skylab:
```
$ skylab
```

## Making Changes

1. Fork the repository on GitHub.

2. Create a new branch from the `master` branch.

3. Make your changes and ensure they follow the project's code style.

The project uses `black` and `isort` to enforce consistent code style. To ensure your changes adhere to the project's code style, you can install `pre-commit` and run it before committing your changes:

```
$ pip install pre-commit
$ pre-commit install
```

4. Test your changes to ensure they work as expected.

5. Push your changes to your forked repository.

6. Submit a pull request from your branch to the `master` branch of the main repository.

## Code of Conduct

The skylab project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating in this project, you are expected to uphold this code. Please report any unacceptable behavior to the project maintainers.

## License

By contributing to the skylab project, you agree that your contributions will be licensed under the project's MIT License.
