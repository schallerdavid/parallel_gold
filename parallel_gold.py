import argparse
import os
import shutil
from subprocess import Popen


logo = '\n'.join(["       v.alpha        _ _     _    ___  ___  _    ___  ",
                  "  _ __  __ _ _ _ __ _| | |___| |  / __|/ _ \| |  |   \ ",
                  " | '_ \/ _` | '_/ _` | | / -_) | | (_ | (_) | |__| |) |",
                  " | .__/\__,_|_| \__,_|_|_\___|_|  \___|\___/|____|___/ ",
                  " |_|                                                   ",
                  "  Run GOLD docking in parallel by splitting the input  ",
                  "         sdf-file and running separate dockings.       ",
                  ""])


def get_sdf_path(gold_conf_path):
    """
    This function extracts the sdf path containing molecules for docking from a gold conf-file.

    Parameters
    ----------
    gold_conf_path : str
        Full path to gold conf-file.

    Returns
    -------
    sdf_path : str
        Full path to sdf-file.
    """
    with open(gold_conf_path, 'r') as rf:
        for line in rf.readlines():
            if 'ligand_data_file' in line:
                return line.strip().split(' ')[1]


def count_sdf_mols(sdf_path):
    """
    This function returns the number of molecules in an sdf-file.
    Parameters

    ----------
    sdf_path : str
        Full path to sdf file.

    Returns
    -------
    counter : int
        Number of molecules.
    """
    counter = 0
    with open(sdf_path, 'r') as sdf_file:
        for line in sdf_file:
            if '$$$$' in line:
                counter += 1
    return counter


def split_sdf_file(input_sdf_path, output_directory, num_files):
    """
    This function splits an sdf-file into smaller sdf-files. Output sdf-files are saved in sequentially numbered
    directories in the output directory.

    Parameters
    ----------
    input_sdf_path : str
        Full path to input sdf-file.
    output_directory : str
        Full path to output directory.
    num_files : int
        Number of output sdf-files to generate.
    """
    num_mols = count_sdf_mols(sdf_path)
    with open(input_sdf_path, 'r') as rf:
        for file_counter in range(num_files):
            mol_counter = 0
            mols_per_file = num_mols // (num_files - file_counter)
            num_mols = num_mols - mols_per_file
            output_sdf_path = os.path.join(os.path.join(output_directory, str(file_counter)),
                                           str(file_counter) + '.sdf')
            with open(output_sdf_path, 'w') as \
                    wf:
                while mol_counter < mols_per_file:
                    line = rf.readline()
                    wf.write(line)
                    if '$$$$' in line:
                        mol_counter += 1
    return


def make_directories(output_directory, num_directories):
    """
    This function makes sequentially numbered directories.

    Parameters
    ----------
    output_directory : str
        Full path to output directory.
    num_directories : int
        Number of output directories.
    """
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)
    for directory_counter in range(num_directories):
        directory = os.path.join(output_directory, str(directory_counter))
        os.makedirs(directory)
    return


def run_docking(output_directory, num_processes, gold_conf_path):
    """
    This function runs docking with GOLD.

    Parameters
    ----------
    output_directory : str
        Full path to output directory.
    num_processes : int
        Number of parallel GOLD dockings.
    gold_conf_path : str
        Full path to gold conf-file.
    """
    processes = []
    for process_counter in range(num_processes):
        gold_conf_path_edit = os.path.join(os.path.join(output_directory, str(process_counter)), 'gold.conf')
        with open(gold_conf_path, 'r') as rf:
            with open(gold_conf_path_edit, 'w') as wf:
                for line in rf.readlines():
                    if 'ligand_data_file' in line:
                        num_poses = line.strip().split(' ')[-1]
                        input_sdf_path = os.path.join(os.path.join(output_directory, str(process_counter)),
                                                      str(process_counter) + '.sdf')
                        wf.write('ligand_data_file {} {}\n'.format(input_sdf_path, num_poses))
                    elif 'concatenated_output' in line:
                        output_sdf_path = os.path.join(os.path.join(output_directory, str(process_counter)),
                                                       'results.sdf')
                        wf.write('concatenated_output {}\n'. format(output_sdf_path))
                    else:
                        wf.write(line)
        os.chdir(os.path.join(output_directory, str(process_counter)))
        processes.append(Popen('gold_auto gold.conf', shell=True))
    for process in processes:
        process.wait()
    return


if __name__ == "__main__":
    description = 'Run GOLD docking in parallel by splitting the input sdf-file and running separate dockings.'
    parser = argparse.ArgumentParser(prog='moldbprep', description=description,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-g', dest='gold_conf_path', help='path to gold config file', required=True)
    parser.add_argument('-o', dest='output_directory', help='path to output directory', default='output')
    parser.add_argument('-p', dest='num_processes', help='number of parallel processes', default=1)
    parser.add_argument('-c', dest='clean', action='store_true', help='Merge results and clean directory')
    gold_conf_path = os.path.abspath(parser.parse_args().gold_conf_path)
    output_directory = os.path.abspath(parser.parse_args().output_directory)
    num_processes = int(parser.parse_args().num_processes)
    clean = parser.parse_args().clean
    sdf_path = get_sdf_path(gold_conf_path)
    make_directories(output_directory, num_processes)
    split_sdf_file(sdf_path, output_directory, num_processes)
    run_docking(output_directory, num_processes, gold_conf_path)
    # cleaning is missing
