# Quick start with translated transctipts  
  
  
```bash
orthofinder -f Example
  
python singlecopy_from_OrthoFinder.py Example Singlecopy 11  
  
python prank_Wrapper Singlecopy  
  
python phyutility_Wrapper.py Singlecopy 0.3  
  
python supermatrix_concatenate.py Singlecopy 150 11 Dinoflagellate_21species_phylotranscritpomic_supermatrix  
  
iqtree -s Dinoflagellate_21species_phylotranscritpomic_supermatrix.phy -spp Dinoflagellate_21species_phylotranscritpomic_supermatrix.model -m LG+C60+R+F -bb 1000 -nt 32
  
```
