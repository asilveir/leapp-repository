from leapp.libraries.actor import library


class logger_mocked(object):
    def __init__(self):
        self.infomsg = None

    def info(self, *args):
        self.infomsg = args

    def __call__(self):
        return self


def test_file_not_read(monkeypatch):
    def is_file_readable_mocked(path):
        return False

    monkeypatch.setattr(library, '_is_file_readable', is_file_readable_mocked)
    assert library.read_nm_config('unreadable_file') is None


def test_nm_with_dchp(monkeypatch):
    s = library.read_nm_config(file_path='tests/files/nm_cfg_with_dhcp')
    parser = library.parser_nm_config(s)

    assert s is not None
    assert parser is not None
    assert parser.has_option('main', 'dhcp')


def test_nm_without_dchp(monkeypatch):
    s = library.read_nm_config(file_path='tests/files/nm_cfg_without_dhcp')
    parser = library.parser_nm_config(s)

    assert s is not None
    assert parser is not None
    assert parser.has_option('main', 'dhcp') is False


def test_nm_with_error(monkeypatch):
    s = library.read_nm_config(file_path='tests/files/nm_cfg_file_error')
    parser = library.parser_nm_config(s)

    assert s is not None
    assert parser is not None
    assert parser.has_section('main') is False
    assert parser.has_option('main', 'dhcp') is False

