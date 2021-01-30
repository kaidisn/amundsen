import psycopg2
import csv

# connection info
user = 'fshabbir'
host = 'redshift-production.ckzx9cywdjko.us-east-1.redshift.amazonaws.com'
port = '5439'
db = 'redshiftdb'
pw = 'PWD' # replace before running

# path to save data
file_path = '/Users/faizan/Documents/Repo/amundsen/amundsendatabuilder/example/acorns_data/redshift_table_owners.csv'

def setup_connection():
	con=psycopg2.connect(dbname= db, host=host, 
	port= port, user= user, password= pw)
	return con

def execute_query(query):
	cur = con.cursor()
	cur.execute(query)
	results = cur.fetchall()
	cur.close()
	return results

con = setup_connection()
results = execute_query("SELECT schemaname, tablename, tableowner FROM pg_tables;")

# Format results as db_name,schema,cluster,table_name,owners
db_name = 'redshift'
cluster = 'redshiftdb'
formatted_table_owners = [[db_name, x[0], cluster, x[1], '{}@acorns.com'.format(x[2])] for x in results]

# save to CSV
with open(file_path, 'w') as f:
	cwriter = csv.writer(f)
	cwriter.writerows(formatted_table_owners)

con.close()