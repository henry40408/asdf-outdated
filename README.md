# asdf-outdated

outdated plugin for [asdf](https://github.com/asdf-vm/asdf) version manager

## Requirements

### macOS

* Python 3.x: should be built-in in recent versions

### Linux

* Python 3.x

## Install

After installing [asdf](https://github.com/asdf-vm/asdf), install the plugin by running:

```bash
asdf plugin add outdated https://github.com/henry40408/asdf-outdated.git 
```

## Use

Check every plugins in `~/.tool-versions`:

```bash
asdf outdated
```

Check one plugin in `~/.tool-versions`, e.g. `python`:


```bash
asdf outdated python
```

Help:

Print help message.

```bash
asdf outdated -h
```

# License

MIT
