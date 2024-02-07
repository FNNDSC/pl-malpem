#!/usr/bin/env python

import itertools
import subprocess as sp
import sys
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from pathlib import Path

from chris_plugin import chris_plugin

__version__ = '1.3.0'

DISPLAY_TITLE = r"""
       _                        _                      
      | |                      | |                     
 _ __ | |______ _ __ ___   __ _| |_ __   ___ _ __ ___  
| '_ \| |______| '_ ` _ \ / _` | | '_ \ / _ \ '_ ` _ \ 
| |_) | |      | | | | | | (_| | | |_) |  __/ | | | | |
| .__/|_|      |_| |_| |_|\__,_|_| .__/ \___|_| |_| |_|
| |                              | |                   
|_|                              |_|                   
"""


parser = ArgumentParser(description='ChRIS plugin wrapper for the MALPEM brain MRI segmentation pipeline.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-f', '--field_strength', type=str,
                    help='field strength, 1.5T/3T')
parser.add_argument('-c', '--cleanup', action='store_true',
                    help='delete temporary files and atlas deformation fields')
parser.add_argument('-t', '--threads', type=int, default=4,
                    help='maximum number of parallel threads')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')


@chris_plugin(
    parser=parser,
    title='MALPEM Brain Segmentation',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='12Gi',     # supported units: Mi, Gi
    min_cpu_limit='8000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    niftis = find_niftis(inputdir)
    if len(niftis) == 0:
        print('error: no input file found.')
        sys.exit(1)
    if len(niftis) > 1:
        print('error: too many input files found.')
        sys.exit(1)

    print(DISPLAY_TITLE, flush=True)

    cmd = [
        '/opt/malpem-1.3/bin/malpem-proot',
        # caution: the malpem-proot requires -i, -o (instead of --input_file, --output_dir)
        '-i', niftis[0],
        '-o', outputdir,
        '-t', str(options.threads),
    ]
    if options.field_strength is not None:
        cmd.extend(['-f', options.field_strength])
    if options.cleanup:
        cmd.append('-c')

    proc = sp.run(cmd)
    sys.exit(proc.returncode)


def find_niftis(parent_dir: Path) -> list[Path]:
    return [
        *parent_dir.rglob('*.nii.gz'),
        *parent_dir.rglob('*.nii')
    ]


if __name__ == '__main__':
    main()
