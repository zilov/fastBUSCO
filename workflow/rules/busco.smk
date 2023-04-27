rule busco:
    input:
        ASSEMBLY
    conda:
        envs.busco
    threads: workflow.cores
    output:
        f"{OUTDIR}/{PREFIX}.busco"
    params:
        lineage = BUSCO_LINEAGE,
        outdir = OUTDIR,
        mode = MODE,
        tmp_outdir = TMP_OUTDIR,
        specific_busco = f"{OUTDIR}/busco/short_summary.specific*.txt"
    shell:
       """
       cd {params.outdir}
       
       busco \
             --offline \
             -l {params.lineage} \
             -i {input} \
             -o {params.tmp_outdir} \
             -m {params.mode} \
             -f \
             -c {threads}
             
        cp {params.specific_busco} {output}
             """  
