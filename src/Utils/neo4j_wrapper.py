from neo4j import GraphDatabase

# Replace with your Neo4j Aura connection details
uri = "neo4j+s://43c248ae.databases.neo4j.io"
username = "neo4j"  # usually the default username is 'neo4j'
password = "2685ZfD2leQk-K0ny1gKAqGHVlR6OQWfXbMcjylkJAU"

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