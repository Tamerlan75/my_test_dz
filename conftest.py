import pytest
from checkers import checout
import yaml
import string, random
from datetime import datetime

with open ('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checout(f'mkdir {data["path_in"]} {data["path_out"]} {data["path_ext"]} {data["path_ext2"]}', '')


@pytest.fixture()
def clear_folders():
    return checout(f'rm -rf {data["path_in"]}/* {data["path_out"]}/* {data["path_ext"]}/* {data["path_ext2"]}/*', ' ')


@pytest.fixture()
def make_files():
    list_off_files = []
    for item in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checout(f'cd {data["path_in"]}; dd if=/dev/urandom of={filename} bs={data["bs"]} count=1 iflag=fullblock', ' '):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    if not checout(f'cd {data["path_in"]}; mkdir {subfoldername}', ''):
        return None, None
    if not checout(f'cd {data["path_in"]}/{subfoldername}; dd if=/dev/urandom of={testfilename} bs=1M count=1 iflag=fullblock', ''):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%S:%f")}')
    yield print(f'Stop: {datetime.now().strftime("%H:%M:%S:%f")}')


@pytest.fixture()
def neg_arx():
    checout(f'cd {data["path_in"]}; 7z a {data["path_out"]}/arx3', 'Everything is Ok')
    checout(f'truncate -s 1 {data["path_out"]}/arx3', 'Everything is Ok')
    yield "arx3"
    checout(f'rm -f {data["path_out"]}/arx3.7z', '')


@pytest.fixture(autouse=True)
def add_stat():
    with open('/proc/loadavg', 'r', encoding='utf-8') as f:
        rez = f.read()
    with open('../stat.txt', 'a', encoding='utf-8') as f:
        f.write(f'{datetime.now().strftime("%H:%M:%S")}, {data["count"]}, {data["bs"]}, {rez}, ')