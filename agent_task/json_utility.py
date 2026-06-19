import json
from pathlib import Path


class JSONDB:
    def __init__(self) -> None:
        self.path = Path(__file__).parent / "tasks.json"
        self.data = self.__load_data()

    def __load_data(self):
        data = {}
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
        except Exception as e:
            print(f"Error occured: {e}")
        return data if data else {}

    def __get_tasks(self) -> list:
        return self.data["tasks"] if self.data["tasks"] else []

    def __save_data(self) -> None:
        with open(self.path, "w") as file:
            # print(f"saving {self.data} as json")
            json.dump(self.data, file, indent=4)

    def __update_data_and_save_json(self, tasks: list) -> None:
        self.data["tasks"] = tasks
        self.__save_data()

    def fetch_all_tasks(self) -> list[dict | None]:
        return self.__get_tasks()

    def save_task(self, name: str, description: str, status: str) -> str:
        tasks = self.__get_tasks()
        for task in tasks:
            if name == task["name"]:
                return "task exists with same name"
        tasks.append({"name": name, "description": description, "status": status})
        self.__update_data_and_save_json(tasks=tasks)
        return "new task added"

    def update_task_status(self, name: str, new_status: str) -> bool:
        tasks = self.__get_tasks()
        for task in tasks:
            if task["name"] == name:
                task["status"] = new_status
                self.__update_data_and_save_json(tasks=tasks)
                return True
        return False

    def delete_task(self, name: str) -> bool:
        tasks = self.__get_tasks()
        index_of_task_to_remove = None
        for i, task in enumerate(tasks):
            if task["name"] == name:
                index_of_task_to_remove = i
                break

        if index_of_task_to_remove is not None:
            tasks.pop(index_of_task_to_remove)
        else:
            return False

        self.__update_data_and_save_json(tasks=tasks)
        return True
