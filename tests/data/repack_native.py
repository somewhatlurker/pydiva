from os import environ

# make output reproducible
environ['PYFARC_NULL_IV'] = '1'

from pydiva import pyfarc


with open('fontmap_fnm.farc', 'rb') as f:
    farc = pyfarc.from_stream(f)

farc['farc_type'] = 'FARC'
farc['format'] = 0
farc['flags'] = {'encrypted': True, 'compressed': True}

with open('fontmap_fnm_native.farc', 'wb') as f:
    pyfarc.to_stream(farc, f)


with open('fontmap_m39.farc', 'rb') as f:
    farc = pyfarc.from_stream(f)

farc['farc_type'] = 'FARC'
farc['format'] = 1
farc['flags'] = {'encrypted': True, 'compressed': True}

with open('fontmap_m39_native.farc', 'wb') as f:
    pyfarc.to_stream(farc, f)