# NYC_Restaurant_Inspector_App

 @Author: Priyal Nile   
 Check the working app at Streamlit Cloud: https://nyc-restaurant-inspector-app.streamlit.app/

## 1. Project Description/Highlights: 
- Built a Python-based tool using NYC open data to allow users to search and explore restaurant health inspection records. Implemented OOP design with file handling, filtering, and CLI interface. 
- Used public datasets, handled 100k+ records efficiently, and added error logging and search features. 
- About Dataset: https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j/about_data
    - Data Provided by: Department of Health and Mental Hygiene (DOHMH). New York City Restaurant Inspection Results
    - Updated as of: 28 May 2025
    - Notes:
        - Only restaurants in an active status are included in the dataset.
        - Total Rows: 287K
        - Total Columns: 27
        - Each row is a restaurant citation.


## 2. Project Structure:
- readme.md: 

## 3. Learnings: 
- Key Python Concepts:
    - File handling,
    - APIs/Scraping,
    - OOP,
    - CLI/UI,
    - Data Filtering,
    - Error Handling

- Additional Learnings:
    - Git & GitHub Setup & Commands,
    - VSCode Setup and Python ENV Configuration,
    - Streamlit: User Interface for Quick Proof Of Concepts

## 4. Installation: 


1. Create Repo in GitHub and then in your local machine VSCode Try following:

Run following commands in VSCODE -> Project folder (that you created in your system) -> Terminal (Powershell) after you've Logged in to Github & created a Public/Private repository (without README.md file). 
Later, Check by refreshing browser that Github Repository is updated now.

```bash
echo "# NYC_Restaurant_Inspector_App" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/priyalanile/NYC_Restaurant_Inspector_App.git
git push -u origin main
```

3. Setup the Python Environment (env) using the following commands: 
Setting up Python Virtual Environment in VSCODE -> Project folder -> Terminal (DO preferably using CMD i.e. Command Prompt)

- To create a new environment using Conda (Anaconda installation should be in place) from Command prompt in VSCode inside your project directory.

#conda create --name env python=3.9
```bash
conda create -p venv python==3.9 -y 
```
- To check if the environment is created or which all envs are present:
```bash
conda info --envs
```

- To activate this newly created environment using Terminal -> CMD & not powershell: (Note: Generally you get this command ready as a part of venv creation log in above step)

```bash   
conda activate ./venv 

```

- Incase, you want to deactivate the environment: 

```bash
conda deactivate 
```

- Now when within the env environment, if need to install all python libraries present in requirements.txt: 

```bash
pip install -r requirements.txt 
```
pandas
numpy
matplotlib
seaborn
jupyter

- To check which libraries are installed (within Powershell Terminal of VSCode: 
```bash
pip list | Select-String -Pattern "pandas|numpy|matplotlib|seaborn|jupyter"
```

## 5. Usage: 
1. Make sure the Python Environment we created is activated.
```bash
conda activate ./venv
```
2. Run the Streamlit App
```bash
streamlit run appfinal.py OR
streamlit run app.py
```

## 6. Using Git:
```bash
 #after making any changes in the codebase. To see the changes done in which files. Within CMD of VSCode.
 git status

 #To add the changes i.e. to stage the changes. 
 git add .

#To update/commit/ the changes in the main branch
git commit -m "<change description>"

#To push the updated changes into the GitHub:
git push
```

## 6. Possible Future Improvements In this Project: 
- Download as csv downloads entire data. It should only download filtered data.
- In tab 3, we can add a filter to be selected as 'Critical', 'Not Critical' and 'All' to allow us deciding resturants which doesn't have critical flag marked.
- The definition of Grade, Score and Critial flag is repeated in all 3 tabs. INstead of that, we can create a single left side section which is common to all 3 tabs having these details
- Instead of the table as output, we can show a better view, a chart of that restaurant or word cloud of that particular selected restaurant something similar to get view of holistic inspection comments.
- We can further increase the speed of first time loading of the app. As it takes a lot of time now.
- We can further deploy this app in streamlit cloud or on AWS EC2 cluster.


### Additional Important Details:
- GitHub doesn't allow to store/load more than 100MB file. The downloaded version of our data was around 127MB. Hence, we were facing error as ''.
    - To tackle this error, remove the .csv from the GitHub caching and load all data.
    
```bash
git rm --cached nyc_restaurant_inspections.csv
```
  