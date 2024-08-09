from checkers import checout, hash_crc
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
#test_1
    def test_step1(self, make_folders, clear_folders, make_files):
        res_1 = checout(f'cd {data["path_in"]}; 7z a ../out/arx2', 'Everything is Ok')
        res_2 = checout(f'ls {data["path_out"]}', 'arx2.7z')
        assert res_1 and res_2, print('test_1 FAIL')

    #test_2
    def test_step2(self, clear_folders, make_files):
        res = []
        res.append(checout(f'cd {data["path_in"]}; 7z a {data["path_out"]}/arx2', 'Everything is Ok'))
        res.append(checout(f'cd {data["path_out"]}; 7z e arx2.7z -o{data["path_ext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checout(f"ls {data['path_ext']}", item))
        assert all(res), print('test_2 FAIL')
    #test_3
    def test_step3(self):
        assert checout(f'cd {data["path_out"]}; 7z t arx2.7z', 'Everything is Ok'), print('test_1 FAIL')
    #test_4
    def test_step4(self):
        assert checout(f'cd {data["path_in"]}; 7z u arx2.7z', 'Everything is Ok'), print('test_4 FAIL')

    #test_5
    def test_step5(self, clear_folders, make_files):
        res = []
        res.append(checout(f'cd {data["path_in"]}; 7z a ../out/arx2', 'Everything is Ok'))
        for item in make_files:
            res.append(checout(f'cd {data["path_ext"]}; 7z l arx2.7z', item))
        assert all(res), print('test_5 FAIL')

    #test_6
    def test_step6(self, clear_folders, make_files, make_subfolder):
        res = []
        res.append(checout(f'cd {data["path_in"]}; 7z a {data["path_out"]}/arx', 'Everything is Ok'))
        res.append(checout(f'cd {data["path_out"]}; 7z x arx.7z -o {data["path_ext2"] } -y', "Everything is Ok"))
        for item in make_files:
            res.append(checout(f'ls {data["path_ext2"] }', item))

        res.append(checout(f"ls {data['path_ext2'] }", make_subfolder[0]))
        res.append(checout(f"ls {data['path_ext2'] }/{make_subfolder[0]}", make_subfolder[1]))
        assert all(res), print('test_2 FAIL')

    #test_7
    def test_step7(self):
        checout(f'cd {data["path_out"]}; 7z d arx.7z', 'Everything is Ok')

    #test_8
    def test_step8(self, clear_folders, make_files):
        res = []
        for item in make_files:
            res.append(checout(f"cd {data['path_ext']}; 7z h {item}", "Everything is Ok"))
            hash_ = hash_crc(f"cd {data['path_ext']}; crc32 {item}")
            res.append(checout(f"cd {data['path_ext']}; 7z h {item}", 'hash'))
        assert all(res), print('test_2 FAIL')
