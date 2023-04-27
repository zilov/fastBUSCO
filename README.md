# fastBUSCO
The FastBUSCO is a snakemake wrapper is for running BUSCO and removing temporary files, while outputting only summary statistics. It simplifies the process of using BUSCO for genome or protein mode analysis.

## Installation
To use the FastBUSCO Snakemake wrapper, please follow these steps:

Clone the repository to your local machine:

```bash
git clone https://github.com/zilov/fastBUSCO.git
```

Install the required dependencies. Make sure you have Snakemake installed, if not just install it with conda:
```bash
conda install -c bioconda -c conda-forge -c defaults snakemake
```

## Usage
To run the FastBUSCO wrapper, use the following command:

```bash
fastBUSCO.py -m <mode> -f <fasta> -b <busco_lineage> -t <threads> -p <prefix>
```

The wrapper will run BUSCO with the specified parameters and output the summary statistics file named {prefix}.busco in the specified output_folder (or the assembly folder if not provided). Temporary files will be removed after the run.

## Parameters
The FastBUSCO Snakemake wrapper supports the following parameters:

-f, --fasta: Path to the assembly FASTA file. (required)
-m,--mode: Mode to use (choices: "genome", "prot"; default: "genome").
-t, --threads: Number of threads to use (default: 8).
-p, --prefix: Output files prefix (assembly file prefix by default).
-o, --output_folder: Path to the output folder (default: assembly folder).
-b, --busco_lineage: Path to the BUSCO lineage database folder. (required)
-d, --debug: Run in debug mode to check if everything is OK.