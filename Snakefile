#Python script
dictionary = {}
with open("regenotyped_vcf.txt", "r") as file:
	for line in file:
		key, value = line.strip().split("\t")
		dictionary[key] = value


#Rule all
rule all:
    input:
        expand("vcfs/{id}.vcf.gz", id=dictionary.keys()),
        expand("edited_vcfs/{id}.txt", id=dictionary.keys())

# Define the rule for downloading each VCF file
rule download_vcf:
    params:
        url=lambda wildcards: dictionary[wildcards.id]
    output:
        "vcfs/{id}.vcf.gz"
    shell:
        """
        wget -c -nc -O {output} "http://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reproducibility/{params}"
        """

# Rule to process VCF files
rule process_vcf:
    input:
        vcf="vcfs/{id}.vcf.gz"
    output:
        txt="edited_vcfs/{id}.txt"
    shell:
        """
        zcat {input.vcf} | tail -n +17 | awk -F"\t" '{{print $2,$10}}' | awk -F"[ ,::,/]" '{{print $1,$2}}'| sed '1d'  > {output.txt}
        """

