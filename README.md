# MySQLToolkits

A mix toolkits for MySQL.

## Usage

```python
from mysqltoolkit import Client
client = Client(
    host='my_host',
    user='user',
    port=3306,
    password='passwd',
    db='mydb'
)
        
client.insert(
    table='table1',
    fields=['field1', 'field2', 'field2'],
    data=[1, 2, 3]
)
```

