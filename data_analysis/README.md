This is the Notebook used to clean, analyze, and visualize the data presented in our paper: 
# **Vision-Cognition: A tool to measure human occlusion reasoning**

This notebook was written and tested using:    
<a href="www.colab.research.google.com">Google Colab<a/>  

## Recommendations: 

- Make sure that the filename paths of the .csv files match whatever setup you are using. Foor Google Colab, the .csv are located within the same directory as the Jupyter Notebook. For example,you only need to write the following in Colab:

```python
pd.read_csv("foobar.csv")
```
if you want to read the file ```foobar.csv``` into a pandas dataframe. 

The CSV files and the png image you will need to run this notebook can be found on the ```data/``` and ```mnistsamples/``` directories. As stated above, make sure that both of the aformentioned are within the same directory as your Jupyter Notebook.

