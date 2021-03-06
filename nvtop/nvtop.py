#! /usr/bin/env python
"""Runs nvidia-smi to gather all process pids for every NVIDIA-GPU on the 
system and shows a view for every GPU containing both the current GPU 
parameters (temperature, memory use, etc.) and the GPU processes including
user names.

@author Koen Eppenhof
@date 2017/05/13
"""
from nvidia_smi import NvidiaSMI
from gpu_card import GPUCard, Format
import sys
import time

if __name__ == '__main__':
    args = sys.argv[1:]

    # Quit if -h or --help is in the options:
    if '-h' in args or '--help' in args:
        print("""
`nvtop`
-------
Equivalent of the Linux `top` command for NVIDIA GPUs. 

Options
-------
* `nvtop -c` makes the view more compact by leaving out the graphs of the current GPU usage
* `nvtop -g=X` only shows the tables for GPUs in the list X, e.g. nvtop -g=1 only shows GPU 1, nvtop -g=1,2 shows GPUs 1 and 2

These options can be mixed i.e. `nvtop -c -g=1,2,3` shows compact tables for GPUs 1, 2, and 3.

What do the colors mean?
------------------------
The graphs are green when there is low usage, and turn red when they are more than 80% full.
The processes are blue when they are associated with your user name, which helps to distinguish scripts and programs run by yourself.



To quit nvtop, press CTRL-C.

        """)
        quit()

    # Otherwise, initialize an NvidiaSMI parser
    nv = NvidiaSMI()

    # Make compact tables if '-c' is used:
    compact = '-c' in args or '--compact' in args

    # Check if show hidden is turned on
    excluded_users = ['root', 'gdm'] if '-a' not in args else []

    # Select the GPUs in the '-g' option:
    gpus = [x[3:].split(',') for x in args if x[:3] == '-g=']
    if gpus:
        gpus = [int(x.strip()) for x in gpus[0]]

    # Check if the GPU numbers are correct
    valid_gpus = []
    for gpu in gpus:
        if gpu not in range(len(nv.gpu_names)):
            print( 'Invalid GPU id number: {}\n'.format(gpu))
        else:
            valid_gpus.append(gpu)
    if gpus == []:
        valid_gpus = range(len(nv.gpu_names))

    # Print the valid GPU tables
    for gpu_id in valid_gpus:
        card = GPUCard(gpu_id, nv, excluded_users=excluded_users)
        print(card.title_part())
        if not compact:
            print(card.header_part())
        print(card.process_part())
    print(Format.BOLD + (card.line_width - 25) * '-' + ' Press CTRL-C to quit'
        ' ---' + Format.END)
