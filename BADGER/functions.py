import pandas as pd
from sqlite3 import connect
from itables import to_html_datatable

def create_job():
    
    # create config?
    
    pass

### DATATABLES

def job_tables():
    # all
    # active - TODO need status in model
    # completed
    conn = connect("badgerdb.db")    
    df = pd.read_sql("SELECT * FROM job",conn)
    
    # transformations
     # id to be a url TODO ? should this be a decorator?
     
    
    return to_html_datatable(df)

def batch_tables(job_id:int):
    
    conn = connect("badgerdb.db")
    df = pd.read_sql(f"SELECT * FROM batch WHERE job_id={job_id} ORDER BY batch_index DESC")

    return to_html_datatable(df)