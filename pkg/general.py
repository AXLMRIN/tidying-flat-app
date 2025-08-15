def test_function():
    print("## TEST ##")

def get_list_of_tasks():
    """Read the list-of-tasks.txt file and return it's content after cleaning it"""
    # Read
    with open("./data/list-of-tasks.txt", "r") as file:
        all_tasks = file.readlines()
    # Clean
    def clean(task : str) -> str:
        """Remove the dashes and the new lines characters"""
        return task.replace("-", " ").replace("\n", "")
    all_tasks = [clean(task) for task in all_tasks]
    
    return all_tasks
