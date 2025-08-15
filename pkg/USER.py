import os

from .general import name_to_filename

FOLDERNAME = "./data/users"

class User:
    def __init__(self, name : str = "", email : str = "", color : str = "#000000",
            score : float = 0) -> None:
        self.__name = name
        self.__filename = name_to_filename(name)
        self.__path = f"{FOLDERNAME}/{self.__filename}"
        self.__email = email
        self.__color = color
        self.__score = score

    def __str__(self) -> str:
        headline = "## USER ########"
        footline = "#" * len(headline)
        return (
            headline + "\n" +
            self.__name + ' (' + self.__filename + ')\n' +
            self.__email + '\n' +
            self.__color + '\n' +
            'Score: ' + str(self.__score) + "\n" + 
            footline
        )
    
    def __getitem__(self, key : str):
            if key == "name": return self.__name
            elif key == "email": return self.__email
            elif key == "color": return self.__color
            elif key == "score": return self.__score
            else: 
                print(f"ERROR: key {key} does not exist. Return None")
                return None
            
    def __write(self):
        with open(self.__path, "w") as file:
            file.write(self.__name + "\n")
            file.write(self.__email + "\n")
            file.write(self.__color + "\n")
            file.write(str(self.__score) + "\n")

    def save_to_disk(self):
        list_of_existing_users = os.listdir(FOLDERNAME)
        if self.__filename not in list_of_existing_users:
            self.__write()
        else:
            print(f"A file named {self.__filename} already exists.")
            with open(self.__path, "r") as file:
                print(file.readline())
            overwrite : bool = input("Overwrite? [Y]") == "Y"
            if overwrite: self.__write()

    def load_from_disk(self, filename : str) -> None:
        list_of_existing_users = os.listdir(FOLDERNAME)
        if filename in list_of_existing_users:
            with open(f"{FOLDERNAME}/{filename}", "r") as file:
                content = file.readlines()
                #Remove the "\n"
                content = [line.replace("\n", "") for line in content]
            name = content[0]
            email = content[1]
            color = content[2]
            score = float(content[3])
            return User(name, email, color, score)
        else:
            print(f"ERROR: {filename} does not exist in {FOLDERNAME}")
            return None
    
    def get_data(self) -> dict:
        return {
            "name" : self.__name,
            "email" : self.__email,
            "color" : self.__color,
            "score" : self.__score
        }

def get_all_users() -> list[User]:
    list_of_fileneames = os.listdir(FOLDERNAME)
    return [User().load_from_disk(filename) for filename in list_of_fileneames]