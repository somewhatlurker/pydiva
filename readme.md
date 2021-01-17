pydiva
======

Some python (3.8+) stuff for handling files from Project DIVA games.


## pyfarc
Reads and writes farc archives (FArc/FArC/FARC fully supported).  
See `docs/pyfarc.md` for usage.


## pyfmh3
Reads and writes fontmaps for FT and X series games.  
See `docs/pyfmh3.md` for usage.


## pydsc (alpha)
Reads and writes FT dscs, with some limited framework for other games.  
Plans are to document params for many ops so that a more user-friendly editor
application can be made.  
In its current state of completion, it is *not* particularly suitable for long-term stable data storage,
but is enough to prototype a usable text-based dsc editor for example.  
See `docs/pydsc.md` for more information and usage.

　

## Development Info
License is MIT so do whatever you want, but I'd personally prefer if we avoid forks for now.

Format-specific info is in the relevant docs.

### Tests
Run `python -m unittest` from the root directory.