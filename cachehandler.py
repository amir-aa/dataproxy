from pymemcache.client import base
SERVERADDR='127.0.0.1'
# Function for inserting data into Memcached
def insert_data_to_memcached(key, value, expire_time=0):
    try:
        client = base.Client(('localhost', 11211))  # Replace with your Memcached server details
        client.set(key, value, expire=expire_time)
        print(f"Data inserted into Memcached with key: {key}")
    except Exception as e:
        print(f"Failed to insert data into Memcached: {e}")

# Function for retrieving data from Memcached
def retrieve_data_from_memcached(key):
    try:
        client = base.Client(('localhost', 11211))  # Replace with your Memcached server details
        value = client.get(key)
        if value:
            print(f"Retrieved data from Memcached with key {key}: {value}")
            return value
        else:
            print(f"No data found in Memcached with key: {key}")
            return None
    except Exception as e:
        print(f"Failed to retrieve data from Memcached: {e}")
        return None

