# ar4ds
Automated Reasoning For Data Science

## Contributors and Acknowledgements
This project is maintained by the University of Chicago Database Group under P.I Sanjay Krishnan. This work is in part supported by a generous equipment grant from NVIDIA. The following students have contributed to the project.

* Amy Zeng
* Xifan Yu
* Alex Zhao

## Motivation
When is a database query result suprising? Data scientists implicitly ground quantitative results from data in qualitative models of the world.
Suppose our database returns that Fred, a manager, earns more money than John.
The data scientist might justify this result with a series of "soft" logical deductions: (1) Managers usually earn more than other employees, (2) Fred is a manager, (3) therefore it is not unsual that Fred earns more than John. These logical sentences sit in a middle ground between logic and probability called Modal Logic. Modal logic is a type of formal logic from the 1960s that extends classical logic to include operators expressing modality. A modal is a word that qualifies a statement (such as "usually")--more specifically, quantifies the fraction of possible worlds a statement is true.

 In this project, we build a modal logic programming system that extends standard SQL with modal deductions. This allows users performing quantitative data analysis to also synthesize qualitative models (systems of modal rules and deductions) to qualify their quantitative conclusions.

## Requirements
* numpy 1.15
* pandas 0.23 
* astor 0.7


