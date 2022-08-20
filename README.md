[![Tests](https://github.com/tlambert03/napari-plugin-checks/actions/workflows/ci.yml/badge.svg)](https://github.com/tlambert03/napari-plugin-checks/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/tlambert03/napari-plugin-checks/main.svg)](https://results.pre-commit.ci/latest/github/tlambert03/napari-plugin-checks/main)
[![codecov](https://codecov.io/gh/tlambert03/napari-plugin-checks/branch/main/graph/badge.svg?token=yAH5X3lnpx)](https://codecov.io/gh/tlambert03/napari-plugin-checks)


## napari-plugin-checks

A tool (and pre-commit hook) to statically some best practices for napari plugins

For background, read [Best practices when developing napari plugins](https://napari.org/plugins/best_practices.html)


## As a pre-commit hook

See [pre-commit](https://pre-commit.com/) for instructions on using pre-commit.

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/tlambert03/napari-plugin-checks
    rev: v0.3.0
    hooks:
    -   id: napari-plugin-checks
```

## checks

### Don’t include PySide2 or PyQt5 in your plugin’s dependencies.

may break user environment if they use conda pyqt, or use pyside2

```python
# bad setup.cfg
[options]
install_requires =
    PyQt5
```

```python
# good setup.cfg
[options]
install_requires =
    qtpy
```

[details](https://napari.org/plugins/best_practices.html#don-t-include-pyside2-or-pyqt5-in-your-plugin-s-dependencies)

### Don't import directly from PyQt5 import PySide2

```python
# bad
from PyQt5 import QtWidgets
```

```python
# good
from qtpy import QtWidgets
```

- your plugin may not work depending on the environment
