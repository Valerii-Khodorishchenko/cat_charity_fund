import json


def json_ro_env(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    with open('.env', 'a', encoding="utf-8") as env_file:
        for key, value in data.items():
            env_file.write('{}={}\n'.format(key, value.replace('\n', '\\n')))


if __name__ == '__main__':
    json_ro_env('key.json')
