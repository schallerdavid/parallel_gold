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

#### Create alias for your bash or c shell

```bash
echo 'alias parallel_gold="python3 ~/parallel_gold/parallel_gold.py"' >> ~/.bashrc
```
or
```bash
echo 'alias parallel_gold "python3 ~/parallel_gold/parallel_gold.py"' >> ~/.cshrc
```

## Run parallel_gold

Generate a gold.conf-file for your system. The docking poses need to be saved in a single output file (specified as concatenated_output in gold conf-file).

Open a terminal, change to project directory and run parallel_gold.
```bash
cd docking_directory
parallel_gold -g gold.conf -p 6
```

Can be also used to submit jobs via slurm.
```bash
parallel_gold -g gold.conf -s cn-cpu -p 28
```

## Copyright

Copyright (c) 2020, David Schaller
