import os
from neo4j import GraphDatabase

# Replace with your Neo4j Aura connection details
uri = os.getenv('NEO4J_URL')
username = os.getenv('NEO4J_USER')  # usually the default username is 'neo4j'
password = os.getenv('NEO4J_USER')

# Create a driver instance
driver = GraphDatabase.driver(uri, auth=(username, password))


# Define a function to run a simple query
def fetch_data(driver):
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n LIMIT 5")
        for record in result:
            print(record)

# Run the function to fetch and print data
fetch_data(driver)

# Close the driver connection
driver.close()