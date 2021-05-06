# MothurFilter
# Language: Python
# Input: TXT (keyword-value pairs)
# Output: PREFIX
# Tested with: PluMA 1.1, Python 3.6
# Dependency:

PluMA plugin that takes Mothur shared and taxonomy files
and removes all taxa that do not appear in a user-specifie
percentage of samples in each group.

It accepts as input a tab-delimited parameter file of keyword-value
pairs:
shared: Mothur shared file (input)
taxonomy: Mothur taxonomy file (input)
metadata: Table mapping samples to groups
threshold: Percentage threshold
sharedout: Filtered Mothur shared file (output)
taxonomyout: Filtered Mothur taxonomy file (output)

Filtered output files are prefixed by the user-specified output PREFIX.
