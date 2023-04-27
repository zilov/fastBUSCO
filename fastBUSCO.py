#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#@created: 16.02.2023
#@author: Danil Zilov
#@contact: zilov.d@gmail.com

import argparse
import os
import os.path
from inspect import getsourcefile
from datetime import datetime
import yaml
import sys

## generates config file which is used by Snakemake
def config_maker(settings, config_file):
    if not os.path.exists(os.path.dirname(config_file)):
        os.mkdir(os.path.dirname(config_file))
    with open(config_file, "w") as f:
        yaml.dump(settings, f)
        print(f"CONFIG IS CREATED! {config_file}")
        

def check_input(path_to_file):
    if not os.path.isfile(path_to_file) or os.path.getsize(path_to_file) == 0:
        raise ValueError(f"The file '{path_to_file}' does not exist or empty. Check arguemnts list!")
    return os.path.abspath(path_to_file)

def main(settings):        
    if settings["debug"]:
        snake_debug = "-n"
    else:
        snake_debug = ""

    #Snakemake
    command = f"""
    snakemake --snakefile {settings["execution_folder"]}/workflow/Snakefile \
              --configfile {settings["config_file"]} \
              --cores {settings["threads"]} \
              --use-conda {snake_debug}"""
    print(command)
    os.system(command)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run BUSCO and remove tmp files')
    parser.add_argument("-m", "--mode", help="mode to use", 
                        choices=["genome", "prot"], default="genome")
    parser.add_argument('-f', '--fasta', type=str, help='Path to the assembly fasta file.', required=True)
    parser.add_argument('-t','--threads', type=int, help='number of threads [default == 8]', default = 8)
    parser.add_argument('-p', '--prefix', help="output files prefix (assembly file prefix by default)", default='')
    parser.add_argument('-o', '--output_folder', type=str, help='Path to the output folder (default is assembly folder)')
    parser.add_argument('-b','--busco_lineage', help="path to busco lineage database folder", required=True)
    parser.add_argument('-d','--debug', help='debug mode', action='store_true') ## run in debug mode to check if everything is ok
        
    args = parser.parse_args()
    
    ## parse args
    mode = args.mode
    fasta = check_input(args.fasta)
    output_folder = os.path.split(fasta)[0] if not args.output_folder else os.path.abspath(args.output_folder)
    debug = args.debug
    threads = args.threads
    busco_lineage = check_input(args.busco_lineage)
    prefix = os.path.splitext(os.path.basename(assembly))[0] if not args.prefix else args.prefix
    
    ## run settings
    execution_folder = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
    execution_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    config_file = os.path.join(execution_folder, f"config/config_{execution_time}.yaml")
    tmp_outdir = os.path.join(output_folder, f"fastBUSCO_{execution_time}")
    run_folder = os.getcwd()
    command = " ".join(sys.argv)
    
    ## change to execution folder to not regenerate snakemake env files
    os.chdir(execution_folder)
            
    # set settings to create config and run tool
    settings = {
        "command" : command,
        "run_folder": run_folder,
        "mode" : mode,
        "fasta": fasta,
        "outdir" : output_folder,
        "tmp_outdir": tmp_outdir,
        "execution_folder" : execution_folder,
        "prefix" : prefix,
        "debug": debug,
        "config_file" : config_file,
        "threads" : threads
    }
    
    config_maker(settings, config_file)
    main(settings)