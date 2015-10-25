# Topic Modelling For Streetfootballworld Posts

## 

Install [Anaconda](https://www.continuum.io/downloads) (or any other Python distribution with scikit-learn). You might have to install flask-wtf:

    conda install flask-wtf
   

## Get Data

Download entire folder from [Hackpad Site](https://hackpad.com/Streetfootballworld-UwhpkzuhGqn), untar/unzip and put that folder in [rootfolder]

## Train topic model and analyse/save results

This only works if the data is cleaned and stored in pickle file. 

    python [rootfolder]/coderepo/analysis.py
    
## Start flask server

Go to [rootfolder]/coderepo/app and run
    
    python routes.py

Now you can open a browser and to to localhost:5000

