# EViS

An Enhanced Virtual Screening Approach based on Pocket Ligand Similarity

## About EViS

EViS is an enhanced virtual screening method which integrates ligand docking, protein pocket template searching and ligand template shape similarity calculating. A novel **PL-score** to characterize local pocket-ligand template similarity is used to evaluate the screening compounds.
The docking poses (**MOL2 format**) obtained by any docking programs can be evaluated by PL-score comparing with the native pocket-ligand pairs in BioLip dataset.

## Getting Started

### Dependencies and Installing

* Before running **EViS**, the following packages should be installed.
* gcc: gcc-8.3.0
* python version : 2.7
* numpy: numpy 1.16.6 
* git clone: https://github.com/JingHuangLab/EViS.git

### Executing program

EViS program needs two consecutive steps (please ensure the last step was completed before running the next step):

1, prepare the screening compounds (**MOL2 format**) and pocket (**'.POC' format**) into the input folder.

* put all compounds (MOL2 format) into **(/EViS/user_input/results_docking/ligand_mol2/)** subfolder.

* put the pocket file (**named as "nativepocket.poc"**) into the (**/EViS/user_input/results_docking/pocket/**) subfolder.

    The pocket is like as:
```
POC     nativepocket
ATOM    253  N   VAL A  49       6.937   3.497 -28.457  1.00 34.68           N
ATOM    254  CA  VAL A  49       6.465   2.179 -28.887  1.00 34.68           C
ATOM    255  C   VAL A  49       5.665   2.297 -30.179  1.00 34.68           C
ATOM    256  O   VAL A  49       5.965   1.651 -31.192  1.00 34.68           O
...
TRE
```
If you are still not sure the input files, you can check the [example files](user_input/results_docking/) in this repository.

2, runEViS.py

For exmple：
```
cd /EViS/webserver/script/
python runEViS.py
```

output:

pocket folder:
* **pocket_align.POC** : all pocket templates for nativepocket.poc with similarity >0.5
* **pocket_topN.info** : top 50 (maximum) template pockets information
* **pocket_topN.mol2** : the template ligands binding with the topN template pockets in BioLip dataset.

ligands_mol2 folder:
* **.lsalign** ： the similarity file between the screening compound and topN template ligands save in "pocket_topN.mol2"

results_docking folder:
* **PLscore.result** : the final PL-score results for the screening compounds. 


## Help
If you have any questions, please contact with Wenyi Zhang(zhangwenyi@westlake.edu.cn)

## Authors

* Wenyi Zhang (zhangwenyi@westlake.edu.cn)
* JingHuang (Huangjing@westlake.edu.cn)

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [LS-align](https://zhanggroup.org/LS-align/)
* [PPS-align](https://zhanggroup.org/PPS-align/)
* [ITASSER](https://zhanggroup.org/I-TASSER/l)
