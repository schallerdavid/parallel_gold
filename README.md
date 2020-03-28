# parallel_gold
Run GOLD in parallel by splitting the sdf-file containing the ligands for docking into smaller sdf-files and run separate docking jobs.

## Install

#### Clone this repository

Open a new terminal and clone this repository.
```bash
cd ~
git clone https://github.com/schallerdavid/parallel_gold.git
```

#### Dependencies

This tool requires Ṕython>=3.5 and a working GOLD installation. It was only tested on linux. The system needs to be able to handle the alias "gold_auto".

#### Create alias for your bash

```bash
echo 'alias parallel_gold="python3 ~/parallel_gold/parallel_gold.py"' >> ~/.bashrc
```

## Run parallel_gold

Generate a gold.conf-file for your system. The docking poses need to be saved in a single output file.

Open a bash shell, change to project directory and run parallel_gold.
```bash
bash
cd docking_directory
parallel_gold -s ligands_for_docking.sdf -g gold.conf -p 6
```

## Copyright

Copyright (c) 2020, David Schaller
