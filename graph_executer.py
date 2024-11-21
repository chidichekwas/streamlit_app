from graph_generator import generate_graph
from nodes.generate_column_description_node import generate_column_description


def get_reports(user_query, csv_file_path, column_description):
    app = generate_graph()

    # user_query = f"""
    # {user_query}
    # Do it in Python and generate a single report. 
    # Combine numerical analysis with observations, visualizations and charts.
    # If any visualization is needed, save it in images folder with unique file name including uuid.
    # Include the saved image with its RELATIVE PATH in the reports as markdown. 
    # Generate the reports in markdown format (DO NOT INCLUDE ```markdown) and print the markdown reports.
    # """

    results = app.invoke({
        "query": user_query, 
        "csv_file_path": csv_file_path, 
        "column_description": column_description,
        'Python_script_check': 0, 
        "max_Python_script_check": 5
        })
    if results['execution_error']:
        return f"Execution Error: {results['execution_error']}"
    else:
        return results['reports']
    
def get_column_description(csv_file_path):
    column_description = generate_column_description({"csv_file_path": csv_file_path})
    return column_description["column_description"]
