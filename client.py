import requests


def main_cycle():
    while (True):
        command = [i for i in input("Введите запрос:\n").split()]
        response = ""
        if command[0].__eq__("sozd_zam"):
            response = requests.post(f"http://{HOST}:{PORT}/sozdanie_zametki",
            params={"text": command[1], "token": command[2]})
        if command[0].__eq__("info_zam"):
            response = requests.post(f"http://{HOST}:{PORT}/sozdanie_zametki/{command[1]}/lolo",
            params={"id": command[1], "token": command[2]})
        if command[0].__eq__("read_note"):
            response = requests.get(f"http://{HOST}:{PORT}",
            params={"id": command[1], "token": command[2]})
        if command[0].__eq__("izmen_text"):
            response = requests.post(f"http://{HOST}:{PORT}/",
            params={"id": command[1], "text": command[2], "token": command[3]})
        if command[0].__eq__("delete_zam"):
            response = requests.delete(f"http://{HOST}:{PORT}/sozdanie_zametki/{command[1]}/delete",
            params={"id": command[1], "token": command[2]})
        if command[0].__eq__("list_zam"):
            response = requests.get(f"http://{HOST}:{PORT}/list",
            params={"token": command[1]})

        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")


# Перед запуском этой программы запустить main.py!
if __name__ == '__main__':
    HOST = "localhost"
    PORT = 8080

    main_cycle()

