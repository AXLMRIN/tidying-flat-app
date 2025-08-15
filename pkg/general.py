
def test_function():
    print("## TEST ##")
    with open("./data/list-of-tasks.txt", "r") as file:
        all = file.readlines()
    print(all)
