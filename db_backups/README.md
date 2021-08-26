## Backing Up your Database 
After the data collection phase of Vision-Cognition is done, we recommend backing up the database as a sql dump using the bash script in this repository:

```
sudo bash get-db-dump.sh
```
This bash script assumes that the mysql database you are using has the same name as the one defined in ```../launch-script.sh```. If your database has a different name, modify the script accordingly.
   
Once you have your sql dump, use the  python script to create csv files of the collected data. These files are ready to use in environments like Jupyter Notebook for data analysis, as we did in ```../data_analysis/```.

```
python3 sqldump-to-csv.py [SQL DUMP FILENAME]
```

