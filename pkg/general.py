import os 

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

def name_to_filename(name : str) -> str:
    filename = ''.join(c for c in name if c.isascii())
    return filename + ".txt"

def del_task(filename : str):
    list_of_existing_tasks = os.listdir('./data/tasks')
    if filename in list_of_existing_tasks:
        try:
            os.remove(f"./data/tasks/{filename}")
            print(f"File {filename} was successfully deleted")
        except Exception as e:
            print((f"ERROR: file {filename} exists in ./data/tasks but could not "
                   f"be deleted because:\n{e}"))

    else:
        print(f"ERROR: file {filename} does not exist in ./data/tasks")