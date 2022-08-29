# grana_model
Author: Magnus Wood, Kirchhoff Lab, WSU \n
Date: 2020 onward

## Protein structures in the landscape of a 
Within a plant, there are organelles called chloroplasts. They are tiny structures, only 5 micrometers long(1), but are the location in which light is converted into chemical energy. The interior of the chloroplast is a colorless fluid called stroma, in which float stacks of membrane structures called grana, that look a little like a stack of pancakes. It is in these grana that the light harvesting occurs. 

The grana is made up of individual thylakoid membrane sacs. A single thylakoid is only 200 nm in diameter, and consists of a lipid bilayer membrane surrounding an interior fluid-filled space called a lumen. The protein structures involved in photosynthesis are embedded within this lipid bylayer, and the largest of these protrude slightly outside it to both the interior (the lumen side) and to the exterior (the stroma side). 

We look now inside the thylakoid membrane, from the lumen side. This is the space between the lipid bilayers, where plastiquinone carries electrons from PSII to cytb6f. We see the various structures of the thylakoid arranged: PSII in its many forms, cytb6f, the LHCII light harvesting complex. It is a highly packed city of protein structures. 

We don't know exactly how they are arranged within this landscape, but we know the approximate number of structures from SEM images, and we know the sizes of the structures themselves. Can we build a model that can represent these complex landscapes?

## installation instructions
1. Make sure you have Python 3.9.7 installed on your machine.
2. 'git clone https://github.com/fieryWalrus1002/grana_model.git' in your projects directory. 
3. 'py -m venv venv' will create a virtual environment in the /venv/ subdirectory. 
4. Activate the virtual environment by changing to the /grana_model/ directory in your projects folder and running the following command from the command line 'venv\Scripts\activate' (in Windows 10, its different in Linux). 
4. With (venv) active, run the following command: 'pip install -r requirements.txt'. This will install all packages in requirements.txt that the grana_model package depends on. 
5. (optional) If you would like to modify the module, you'll need the dev packages for testing and debugging. Run the following command: 'pip install -r requirements_dev.txt'
6. (optional) If you have modified the module and want to create new requirements.txt, run 'pip freeze > requirements.txt' to freeze the list of currently installed packages on the venv to a requirements.txt file. 

## version control system: git and github
I use Git for version control. Some basic Git commands are:
```
git status # will return the current git status, ie what has changed from local to remote
git add . # adds all files in the current directory to the git repository
git commit -a -m "commit message" # adds a commit message and commits to the git repository
git push origin # willl push to the git repository at github.com origin, which is the branch
```
(1): Biochemistry, 5th edition. W.H. Freeman and Company. 2002. Found at: https://www.ncbi.nlm.nih.gov/books/NBK22345/, Accessed 9-30-21.