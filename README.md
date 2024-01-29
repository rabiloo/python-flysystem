# Python Flysystem

[![Testing](https://github.com/rabiloo/python-flysystem/actions/workflows/test.yml/badge.svg)](https://github.com/rabiloo/python-flysystem/actions/workflows/test.yml)
[![Latest Version](https://img.shields.io/pypi/v/flysystem.svg)](https://pypi.org/project/flysystem)
[![Downloads](https://img.shields.io/pypi/dm/flysystem.svg)](https://pypi.org/project/flysystem)
[![Pypi Status](https://img.shields.io/pypi/status/flysystem.svg)](https://pypi.org/project/flysystem)
[![Python Versions](https://img.shields.io/pypi/pyversions/flysystem.svg)](https://pypi.org/project/flysystem)

## About Flysystem

[Flysystem](https://github.com/thephpleague/flysystem) is a file storage library for PHP. It provides one interface to interact with many types of filesystems. When you use Flysystem, you're not only protected from vendor lock-in, you'll also have a consistent experience for which ever storage is right for you.

Flysystem is created by [Frank de Jonge](https://github.com/frankdejonge) and https://thephpleague.com/

Python Flysystem is a port of Flysystem for Python

## Install

```
$ pip install flysystem
```

## Usage

```
from flysystem.adapters.local import LocalFilesystemAdapter
from flysystem.filesystem import Filesystem


adapter = LocalFilesystemAdapter(".")
filesystem = Filesystem(adapter)

filesystem.file_exists("/tmp/hello.txt")
```

## Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information on what has changed recently.

## Contributing

Please see [CONTRIBUTING](.github/CONTRIBUTING.md) for details.

## Security Vulnerabilities

Please review [our security policy](../../security/policy) on how to report security vulnerabilities.

## Credits

Special thanks to [Frank de Jonge](https://github.com/frankdejonge) and [Flysystem](https://github.com/thephpleague/flysystem)'s maintainers.

- [Oanh Nguyen](https://github.com/oanhnn)
- [Frank de Jonge](https://github.com/frankdejonge)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE) for more information.
