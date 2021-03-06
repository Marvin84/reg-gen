import sys # Cannot be changed
import os
from os import walk, chown, chmod, path, getenv, makedirs, remove
from sys import platform, exit
from pwd import getpwnam
from distutils import dir_util
from shutil import copy, copytree
import distutils.dir_util
from errno import ENOTDIR
from optparse import OptionParser, BadOptionError, AmbiguousOptionError
from setuptools import setup, find_packages, Extension

"""
Installs the RGT tool with standard setuptools options and additional
options specific for RGT.

Authors: Eduardo G. Gusmao, Manuel Allhoff, Joseph Kuo, Ivan G. Costa.

Installs the RGT tool with standard setuptools options and additional
options specific for RGT.
"""

###################################################################################################
# Unsupported Platforms
###################################################################################################

supported_platforms = ["linux","linux2","darwin"]
if(platform not in supported_platforms):
    print("ERROR: This package currently supports only unix-based systems (Linux and MAC OS X).")
    exit(0)

###################################################################################################
# Parameters
###################################################################################################

"""
Current Version Standard: X.Y.Z
X: Major RGT release.
Y: Major Specific-Tool release.
Z: Minor RGT/Specific-Tool bug corrections.
"""
current_version = "0.0.1"

"""
Tools Dictionary:
  * Insert in the dictionary bellow a key+tuple X: (Y,Z,W,K) representing:
    - X: A string representing the name the user should provide for this script in order to install the tool.
    - Y: A string representing the name of the program which the user should type in the terminal in order to execute the tool.
    - Z: A string representing the path to the main function that executes the program.
    - W: A list with the package requirements for that program.
    - K: A list with external binary files that will be copied by the setup installation function to the user's bin folder.
Tools Dictionary Standard:
  * All programs should start with "rgt-" followed by the program name.
  * The main function called within the script must be termed "main".
"""
if platform.startswith("darwin"):
    bin_dir = "mac"
else:
    bin_dir = "linux"

tools_dictionary = {
"core": (
    None,
    None,
    ["numpy>=1.4.0", "scipy>=0.7.0", "pysam>=0.7.5"],
    ["data/bin/"+bin_dir+"/bedToBigBed","data/bin/"+bin_dir+"/bigBedToBed",
     "data/bin/"+bin_dir+"/wigToBigWig","data/bin/"+bin_dir+"/bigWigMerge",
     "data/bin/"+bin_dir+"/bedGraphToBigWig","data/bin/"+bin_dir+"/bigWigSummary"]
),
"motifanalysis": (
    "rgt-motifanalysis",
    "rgt.motifanalysis.Main:main",
    ["numpy>=1.4.0","scipy>=0.7.0","Biopython>=1.64","pysam>=0.7.5","fisher>=0.1.4"],
    ["data/bin/"+bin_dir+"/bedToBigBed","data/bin/"+bin_dir+"/bigBedToBed"]
), 
"hint": (
    "rgt-hint",
    "rgt.HINT.Main:main",
    ["numpy>=1.4.0","scipy>=0.7.0","scikit-learn>=0.14","hmmlearn>=0.1.1","pysam>=0.7.5"],
    []
), 
"ODIN": (
    "rgt-ODIN",
    "rgt.ODIN.ODIN:main",
    ["hmmlearn<0.2.0", "scikit-learn", "numpy>=1.10.4", "scipy>=0.7.0", "pysam>=0.8.2", "HTSeq", "mpmath"],
    ["data/bin/"+bin_dir+"/wigToBigWig"]
), 
"THOR": (
    "rgt-THOR",
    "rgt.THOR.THOR:main",
    ["hmmlearn<0.2.0", "scikit-learn>=0.17.1", "numpy>=1.10.4", "scipy>=0.7.0", "pysam>=0.8.2", "HTSeq", "mpmath"],
    ["data/bin/"+bin_dir+"/wigToBigWig","data/bin/"+bin_dir+"/bigWigMerge",
    "data/bin/"+bin_dir+"/bedGraphToBigWig"]
),                 
"filterVCF": (
    "rgt-filterVCF",
    "rgt.filterVCF.filterVCF:main",
    ["PyVCF", "numpy>=1.4.0", "scipy>=0.7.0"],
    []
),
"viz": (
    "rgt-viz",
    "rgt.viz.Main:main",
    ["numpy>=1.4.0","scipy>=0.7.0","matplotlib>=1.1.0", "pysam>=0.7.5","matplotlib_venn"],
    ["data/bin/"+bin_dir+"/bigWigSummary"]
),
"TDF": (
    "rgt-TDF",
    "rgt.triplex.Main:main",
    ["numpy>=1.4.0","scipy>=0.7.0","matplotlib>=1.1.0", "pysam>=0.7.5"],
    []
)
}


###################################################################################################
# Auxiliary Functions/Classes
###################################################################################################

# PassThroughOptionParser Class
class PassThroughOptionParser(OptionParser):
    """
    An unknown option pass-through implementation of OptionParser.
    When unknown arguments are encountered, bundle with largs and try again,
    until rargs is depleted.
    sys.exit(status) will still be called if a known argument is passed
    incorrectly (e.g. missing arguments or bad argument types, etc.)
    """
    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self,largs,rargs,values)
            except (BadOptionError,AmbiguousOptionError), e:
                largs.append(e.opt_str)

# recursive_chown_chmod Function
def recursive_chown_chmod(path_to_walk, uid, gid, file_permission, path_permission):
    """
    Recursively applies chown from path.
    """
    for root_dir, directory_list, file_list in walk(path_to_walk):
        chown(root_dir, uid, gid)
        chmod(root_dir, path_permission)
        for f in file_list:
            current_complete_file = path.join(root_dir,f)
            chown(current_complete_file, uid, gid)
            chmod(current_complete_file, file_permission)

###################################################################################################
# Processing Input Arguments
###################################################################################################

# Parameters
rgt_data_base_name = "rgtdata"
usage_message = "python setup.py install [python options] [RGT options]"
version_message = "Regulatory Genomics Toolbox (RGT). Version: "+str(current_version)

# Initializing Option Parser
parser = PassThroughOptionParser(usage = usage_message, version = version_message)

# Parameter: RGT Data Location
param_rgt_data_location_name = "--rgt-data-path"
parser.add_option(param_rgt_data_location_name, type = "string", metavar="STRING",
                  help = "Path containing data used by RGT tool.",
                  dest = "param_rgt_data_location", default = path.join(getenv('HOME'),rgt_data_base_name))

# Parameter: Tool
param_rgt_tool_name = "--rgt-tool"
parser.add_option(param_rgt_tool_name, type = "string", metavar="STRING",
                  help = ("The tool which will be installed. If this argument is not used, "
                          "then the complete package is installed. The current available options"
                          "are: "+", ".join(tools_dictionary.keys())+"; where 'core' means that"
                          "only the RGT python library will be installed with no further command-line"
                          "tools. You can also provide multiple tools in a list separated by comma."), 
                  dest = "param_rgt_tool", default = ",".join(tools_dictionary.keys()))

# Processing Options
options, arguments = parser.parse_args()
if(path.basename(options.param_rgt_data_location) != rgt_data_base_name):
    options.param_rgt_data_location = path.join(options.param_rgt_data_location,rgt_data_base_name)
if(options.param_rgt_data_location[0] == "~"):
    options.param_rgt_data_location = path.join(getenv('HOME'),options.param_rgt_data_location[2:])
options.param_rgt_tool = options.param_rgt_tool.split(",")

# Manually Removing Additional Options from sys.argv
new_sys_argv = []
for e in sys.argv:
    if(param_rgt_data_location_name == e[:len(param_rgt_data_location_name)]): continue
    elif(param_rgt_tool_name == e[:len(param_rgt_tool_name)]): continue
    new_sys_argv.append(e)

sys.argv = new_sys_argv

# Defining entry points
current_entry_points = {"console_scripts" : []}
for tool_option in options.param_rgt_tool:
    if(tool_option != "core"):
        current_entry_points["console_scripts"].append(" = ".join(tools_dictionary[tool_option][:2]))

# Defining install requirements
current_install_requires = []
for tool_option in options.param_rgt_tool: current_install_requires += tools_dictionary[tool_option][2]

###################################################################################################
# Creating Data Path
###################################################################################################

# Creating Data Path
if not path.exists(options.param_rgt_data_location):
    makedirs(options.param_rgt_data_location)

# Creating data.config
data_config_file_name = path.join(options.param_rgt_data_location, "data.config")
if not os.path.isfile(data_config_file_name):
    data_config_file = open(data_config_file_name,"w")
    genome = "mm9"
    genome_dir = path.join(options.param_rgt_data_location, genome)
    data_config_file.write("["+genome+"]\n")
    data_config_file.write("genome: "+path.join(genome_dir,"genome_mm9.fa\n"))
    data_config_file.write("chromosome_sizes: "+path.join(genome_dir,"chrom.sizes.mm9\n"))
    data_config_file.write("gene_regions: "+path.join(genome_dir,"genes_mm9.bed\n"))
    data_config_file.write("annotation: "+path.join(genome_dir,"gencode.vM1.annotation.gtf\n"))
    data_config_file.write("gene_alias: "+path.join(genome_dir,"alias_mouse.txt\n\n"))
    genome = "hg19"
    genome_dir = path.join(options.param_rgt_data_location, genome)
    data_config_file.write("["+genome+"]\n")
    data_config_file.write("genome: "+path.join(genome_dir,"genome_hg19.fa\n"))
    data_config_file.write("chromosome_sizes: "+path.join(genome_dir,"chrom.sizes.hg19\n"))
    data_config_file.write("gene_regions: "+path.join(genome_dir,"genes_hg19.bed\n"))
    data_config_file.write("annotation: "+path.join(genome_dir,"gencode.v19.annotation.gtf\n"))
    data_config_file.write("gene_alias: "+path.join(genome_dir,"alias_human.txt\n\n"))
    genome = "hg38"
    genome_dir = path.join(options.param_rgt_data_location, genome)
    data_config_file.write("["+genome+"]\n")
    data_config_file.write("genome: "+path.join(genome_dir,"genome_hg38.fa\n"))
    data_config_file.write("chromosome_sizes: "+path.join(genome_dir,"chrom.sizes.hg38\n"))
    data_config_file.write("gene_regions: "+path.join(genome_dir,"genes_hg38.bed\n"))
    data_config_file.write("annotation: "+path.join(genome_dir,"gencode.v24.annotation.gtf\n"))
    data_config_file.write("gene_alias: "+path.join(genome_dir,"alias_human.txt\n\n"))
    genome = "zv9"
    genome_dir = path.join(options.param_rgt_data_location, genome)
    data_config_file.write("["+genome+"]\n")
    data_config_file.write("genome: "+path.join(genome_dir,"genome_zv9_ensembl_release_79.fa\n"))
    data_config_file.write("chromosome_sizes: "+path.join(genome_dir,"chrom.sizes.zv9\n"))
    data_config_file.write("gene_regions: "+path.join(genome_dir,"genes_zv9.bed\n"))
    data_config_file.write("annotation: "+path.join(genome_dir,"Danio_rerio.Zv9.79.gtf\n"))
    data_config_file.write("gene_alias: "+path.join(genome_dir,"alias_zebrafish.txt\n\n"))
    genome = "zv10"
    genome_dir = path.join(options.param_rgt_data_location, genome)
    data_config_file.write("["+genome+"]\n")
    data_config_file.write("genome: "+path.join(genome_dir,"genome_zv10_ensembl_release_84.fa\n"))
    data_config_file.write("chromosome_sizes: "+path.join(genome_dir,"chrom.sizes.zv10\n"))
    data_config_file.write("gene_regions: "+path.join(genome_dir,"genes_zv10.bed\n"))
    data_config_file.write("annotation: "+path.join(genome_dir,"Danio_rerio.GRCz10.84.gtf\n"))
    data_config_file.write("gene_alias: "+path.join(genome_dir,"alias_zebrafish.txt\n\n"))
    genome = "self_defined"
    genome_dir = path.join(options.param_rgt_data_location, genome)
    data_config_file.write("["+genome+"]\n")
    data_config_file.write("genome: undefined\n")
    data_config_file.write("chromosome_sizes: undefined\n")
    data_config_file.write("gene_regions: undefined\n")
    data_config_file.write("annotation: undefined\n")
    data_config_file.write("gene_alias: undefined\n\n")
    # data_config_file.write("[GenomeData]\n")
    # data_config_file.write("genome: genome.fa\n")
    # data_config_file.write("chromosome_sizes: chrom.sizes\n")
    # data_config_file.write("association_file: association_file.bed\n")
    # data_config_file.write("gencode_annotation: gencode_annotation.gtf\n")
    # data_config_file.write("gene_alias: alias.txt\n\n")
    data_config_file.write("[MotifData]\n")
    data_config_file.write("pwm_dataset: motifs\n")
    data_config_file.write("logo_dataset: logos\n")
    data_config_file.write("repositories: jaspar_vertebrates,uniprobe_primary\n\n")
    data_config_file.write("[HmmData]\n")
    data_config_file.write("default_hmm_dnase: fp_hmms/dnase.hmm\n")
    data_config_file.write("default_hmm_dnase_bc: fp_hmms/dnase_bc.hmm\n")
    data_config_file.write("default_hmm_histone: fp_hmms/histone.hmm\n")
    data_config_file.write("default_hmm_dnase_histone: fp_hmms/dnase_histone.hmm\n")
    data_config_file.write("default_hmm_dnase_histone_bc: fp_hmms/dnase_histone_bc.hmm\n")
    data_config_file.write("default_bias_table_F: fp_hmms/single_hit_bias_table_F.txt\n")
    data_config_file.write("default_bias_table_R: fp_hmms/single_hit_bias_table_R.txt\n\n")
    
    data_config_file.close()


# Creating data.config.path
script_dir = path.dirname(path.abspath(__file__))
data_config_path_file_name = path.join(script_dir,"rgt","data.config.path")
data_config_path_file = open(data_config_path_file_name,"w")
data_config_path_file.write(data_config_file_name)
data_config_path_file.close()

# Copying data from package folder to installation folder
"""
Copy Files Dictionary:
  * Insert in the dictionary below a key + list in the format X:[Y1,Y2,...Yn], representing:
    - X: A path in the data folder structure.
    - Y1,Y2,...Yn: files/folders inside the path X to be copied.
"""
copy_files_dictionary = {
".": ["setupGenomicData.py","setupLogoData.py"],
"hg19": ["genes_hg19.bed","chrom.sizes.hg19","alias_human.txt"],
"hg38": ["genes_hg38.bed","chrom.sizes.hg38","alias_human.txt"],
"mm9": ["genes_mm9.bed","chrom.sizes.mm9","alias_mouse.txt"],
"zv9": ["genes_zv9.bed","chrom.sizes.zv9","alias_zebrafish.txt"],
"zv10": ["genes_zv10.bed","chrom.sizes.zv10","alias_zebrafish.txt"],
"fp_hmms": ["dnase.hmm", "dnase_bc.hmm", "histone.hmm", "dnase_histone.hmm", "dnase_histone_bc.hmm", "single_hit_bias_table_F.txt", "single_hit_bias_table_R.txt"],
"motifs": ["jaspar_vertebrates", "uniprobe_primary", "uniprobe_secondary", "hocomoco", "hocomoco.fpr", "jaspar_vertebrates.fpr", "uniprobe_primary.fpr", "uniprobe_secondary.fpr"],
"fig": ["rgt_logo.gif","style.css","default_motif_logo.png","jquery-1.11.1.js","jquery.tablesorter.min.js","tdf_logo.png", "viz_logo.png"],
}
for copy_folder in copy_files_dictionary.keys():
    copy_dest_path = path.join(options.param_rgt_data_location,copy_folder)
    if not path.exists(copy_dest_path): makedirs(copy_dest_path)
    for copy_file in copy_files_dictionary[copy_folder]:
        copy_source_file = path.join(script_dir,"data",copy_folder,copy_file)
        copy_dest_file = path.join(copy_dest_path,copy_file)
        if os.path.isfile(copy_source_file):
            copy(copy_source_file, copy_dest_file)
        else:
            dir_util.copy_tree(copy_source_file, copy_dest_file)
        
        # if not path.exists(copy_dest_file): 
        # try: dir_util.copy_tree(copy_source_file, copy_dest_file)
        # except OSError as exc:
        #     if exc.errno == ENOTDIR: 
        #         copy(copy_source_file, copy_dest_file)
        #     else:
        #         raise
    
###################################################################################################
# Setup Function
###################################################################################################

# Parameters
short_description = "Toolkit to perform regulatory genomics data analysis"
classifiers_list = ["Topic :: Scientific/Engineering :: Bio-Informatic",
                    "Topic :: Scientific/Engineering :: Artificial Intelligence"]
keywords_list = ["ChIP-seq","DNase-seq","Peak Calling","Motif Discovery","Motif Enrichment","HMM"]
author_list = ["Eduardo G. Gusmao","Manuel Allhoff","Chao-Chung Kuo","Ivan G. Costa"]
corresponding_mail = "software@costalab.org"
license_type = "GPL"
package_data_dictionary = {"rgt": [path.basename(data_config_path_file_name)]}

# External scripts
external_scripts=[]
for tool_option in options.param_rgt_tool:
    for e in tools_dictionary[tool_option][3]: external_scripts.append(e)

# Fetching Additional Structural Files
readme_file_name = path.join(path.dirname(path.abspath(__file__)), "README.txt")

# Fetching Long Description
readme_file = open(readme_file_name,"r")
long_description =readme_file.read() + "nn"
readme_file.close()

# Setup Function


setup(name = "RGT",
      version = current_version,
      description = short_description,
      long_description = long_description,
      classifiers = classifiers_list,
      keywords = ", ".join(keywords_list),
      author = ", ".join(author_list),
      author_email = corresponding_mail,
      license = license_type,
      packages = find_packages(),
      package_data = package_data_dictionary,
      entry_points = current_entry_points,
      install_requires = current_install_requires,
      scripts = external_scripts )
###################################################################################################
# Termination
###################################################################################################

# Removing data.config.path
remove(data_config_path_file_name)

# Modifying Permissions when Running Superuser/Admin
# $SUDO_USER exists only if you are sudo, and returns the original user name
current_user = getenv("SUDO_USER")
default_file_permission = 0644
default_path_permission = 0755

if(current_user):
    current_user_uid = getpwnam(current_user).pw_uid
    current_user_gid = getpwnam(current_user).pw_gid
    recursive_chown_chmod(options.param_rgt_data_location,current_user_uid,current_user_gid,default_file_permission,default_path_permission)
