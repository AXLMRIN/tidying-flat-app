import os

from general import name_to_filename

FOLDERNAME = "./data/tasks"

class Task:
    def __init__(self, name : str = "", description : str = "", frequency : float = 0) -> None:
        self.__name = name
        self.__filename = name_to_filename(name)
        self.__path = f"{FOLDERNAME}/{self.__filename}"
        self.__description = description
        self.__frequency = frequency


    def __str__(self) -> str:
        return (self.__name + ' (' + self.__filename + ')\n' + self.__description +
            '\n' + 'every ' + str(self.__frequency) + " weeks")

    def __write(self):
        with open(self.__path, "w") as file:
            file.write(self.__name + "\n")
            file.write(self.__description + "\n")
            file.write(str(self.__frequency) + "\n")

    def save_to_disk(self):
        list_of_existing_tasks = os.listdir(FOLDERNAME)
        if self.__filename not in list_of_existing_tasks:
            self.__write()
        else:
            print(f"A file named {self.__filename} already exists.")
            with open(self.__path, "r") as file:
                print(file.readline())
            overwrite : bool = input("Overwrite? [Y]") == "Y"
            if overwrite: self.__write()

    def load_from_disk(self, filename : str) -> None:
        list_of_existing_tasks = os.listdir(FOLDERNAME)
        if filename in list_of_existing_tasks:
            with open(f"{FOLDERNAME}/{filename}", "r") as file:
                content = file.readlines()
                #Remove the "\n"
                content = [line.replace("\n", "") for line in content]
            self.__name = content[0]
            self.__filename = name_to_filename(self.__name)
            self.__path = f"{FOLDERNAME}/{self.__filename}"
            self.__description = content[1]
            self.__frequency = float(content[2])
        else:
            print(f"ERROR: {filename} does not exist in {FOLDERNAME}")