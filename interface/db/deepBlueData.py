# Load data from DeepBlue and store it in a database
# The most important DeepBlue entity is the experiment
# An experiment contains the Epigenetic Data with their metadata

# Use the library xmlrpclib to access the DeepBlue Server in Python 2.7
import xmlrpclib
import sqlite3


# data normalization function, ensures consistency between experiments
# you can add further normalization of experiment, meta or sample data here
def normalizeDeepBlueData(experiment):
	# WGSBS is the same as WGBS -> normalize to WGBS
	if experiment['technique'] == 'WGSBS':
		experiment['technique'] = 'WGBS'

	return experiment


# Accessing DeepBlue

# Set up the client
# Server will be used to access the DeepBlue server
url = "http://deepblue.mpi-inf.mpg.de/xmlrpc"
server = xmlrpclib.Server(url, encoding='UTF-8', allow_none=True)

# As key use the anonymous key or an own user key
user_key = "anonymous_key"


# Experiments can be listed using the list_experiments command
# The command has 6 paramenter: genome assembly, epigenetic mark, sample ID, technique, project, and user_key (except user_key all parameters are optional)

# List all experiments without any filter
print "Querying DeepBlue for experiments..."
(status, experiments) = server.list_experiments("", "", "", "", "", "", "", user_key)
n_exp = len(experiments)

print "Got "+str(n_exp)+" experiments."

# Creation of a database and storage of metadata

# Create a connection object that represents the database
# The database is created automatically if it does not exist
conn = sqlite3.connect('deepBlue.db')

# Create a cursor object
c = conn.cursor()

# Create table structure as defiend in structure file
print "Creating database structure..."
with open('deepBlueStructure.sql','r') as tableStructure:
	c.executescript(tableStructure.read())
print "Done. Inserting experiments..."

# Insert a row of data
# In a pass the metadata of an experiment is stored in the database
for i in range(0, n_exp):
	if i%1000 == 0 and i > 0:
		print "Inserted "+str(i)+"/"+str(n_exp)+" experiments..."

	# Command info lists the metadata of experiments
	(status, info) = server.info(experiments[i][0], user_key)

	experiment = normalizeDeepBlueData(info[0])

	# Insert data of experiment[i][0] in table 'experiments'	
	experiments_data = [experiment['_id'], experiment['name'], experiment['description'], experiment['genome'], experiment['epigenetic_mark'], experiment['sample_id'], experiment['technique'], experiment['project'], experiment['data_type'], experiment['type'], experiment['format']]
	c.execute("INSERT INTO experiments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", experiments_data)
	
	# Insert data of experiment[i][0] in table 'sample_id'	
	sample_info = experiment['sample_info']
	for j in range (0, len(sample_info)):	
		sample_info_data = [experiment['sample_id'], sample_info.keys()[j], sample_info.values()[j]]
		c.execute("INSERT OR IGNORE INTO sample_info VALUES (?, ?, ?)", sample_info_data)
	
	# Insert data of experiment[i][0] in table 'extra_metadata'
	metadata = experiment['extra_metadata']
	for k in range (0, len(metadata)):
		extra_metadata_data = [experiment['_id'], metadata.keys()[k], metadata.values()[k]]
		c.execute("INSERT OR IGNORE INTO extra_metadata VALUES (?, ?, ?)", extra_metadata_data)


print "Inserted a total of "+str(i+1)+"/"+str(n_exp)+" experiments"
print "Commiting database transaction..."

# Save (commit) the changes
conn.commit()

# Close the connection
# Just be sure any changes have been committed or they will be lost
conn.close()

print "Done"