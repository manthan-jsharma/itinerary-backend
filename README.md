## Running the Application

### Setting Up the Environment

1. Create a `.env` file with your database connection string:
   "DATABASE_URL=postgresql://username:password@localhost:5432/thailand_travel"

2. Install the required dependencies: ```shellscript
   pip install -r requirements.txt.

````

3. Run the database migrations:


```shellscript
alembic upgrade head
````
3. Configure both the MCP Server and main app Server, look at the code in run.py file

4. Start the application:

```shellscript
python run.py
```

This will start both the main API server on port 8000 and the MCP server on port 8001.
