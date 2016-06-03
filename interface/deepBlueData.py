import sqlite3
import xmlrpclib

# Connect to DeepBlue
# Before going further, the client must be set up
url = "http://deepblue.mpi-inf.mpg.de/xmlrpc"
server = xmlrpclib.Server(url, encoding='UTF-8', allow_none=True)

# As key use the anonymous key or an own user key
user_key = "anonymous_key"

# List all experiments without filters
(status, experiments) = server.list_experiments("", "", "", "", "", "", "", user_key)


# Creation of a database and storing data
# Create a connection object that represents the database
# Database is created automatically if it does not exist
conn = sqlite3.connect('deepBlue.db')

# Create a cursor object
c = conn.cursor()


# Create table
c.execute('''CREATE TABLE IF NOT EXISTS experiments
     	(_id VARCHAR(255) NOT NULL, 
	name text NOT NULL, 
	description text NOT NULL, 
	genome VARCHAR(255) NOT NULL, 
	epigenetic_mark text NOT NULL,
	sample_id VARCHAR(255) NOT NULL,
	technique VARCHAR(255) NOT NULL,
	project text NOT NULL,
	data_type VARCHAR(255) NOT NULL,
	type VARCHAR(255) NOT NULL,
	format text NOT NULL,
	PRIMARY KEY (_id) )''')

c.execute('''CREATE TABLE IF NOT EXISTS sample_info
     	(sample_id VARCHAR(255) NOT NULL,
	key VARCHAR(255) NOT NULL, 
	value VARCHAR(255) NOT NULL, 
	PRIMARY KEY (sample_id, key) )''')

c.execute('''CREATE TABLE IF NOT EXISTS extra_metadata
     	(experiment_id VARCHAR(255) NOT NULL,
	key VARCHAR(255) NOT NULL,
	value VARCHAR(255) NOT NULL,
	PRIMARY KEY (experiment_id, key) )''')


# Insert a row of data
for i in range(0, len(experiments)):
	(status, info) = server.info(experiments[i][0], user_key)
	# Insert data in table 'experiments'	
	experiments_data = [info[0]['_id'], info[0]['name'], info[0]['description'], info[0]['genome'], info[0]['epigenetic_mark'], info[0]['sample_id'], info[0]['technique'], info[0]['project'], info[0]['data_type'], info[0]['type'], info[0]['format']]
	c.execute("INSERT INTO experiments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", experiments_data)
	
	# Insert dataset j in table 'sample_id'	
	sample_info = info[0]['sample_info']
	for j in range (0, len(sample_info)):	
		sample_info_data = [info[0]['sample_id'], sample_info.keys()[j], sample_info.values()[j]]
		c.execute("INSERT OR IGNORE INTO sample_info VALUES (?, ?, ?)", sample_info_data)
	
	# Insert dataset k in table 'extra_metadata'
	metadata = info[0]['extra_metadata']
	for k in range (0, len(metadata)):
		extra_metadata_data = [info[0]['_id'], metadata.keys()[k], metadata.values()[k]]
		c.execute("INSERT OR IGNORE INTO extra_metadata VALUES (?, ?, ?)", extra_metadata_data)


# Save (commit) the changes
conn.commit()

# Close the connection
# Just be sure any changes have been committed or they will be lost
conn.close()
