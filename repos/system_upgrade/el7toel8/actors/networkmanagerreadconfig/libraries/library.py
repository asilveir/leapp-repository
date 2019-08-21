import os

from six.moves.configparser import ConfigParser, ParsingError

from leapp.libraries.stdlib import CalledProcessError, run, api


def _is_file_readable(path):
    ''' Verify if file exists and is readable '''
    return os.path.isfile(path) and os.access(path, os.R_OK)


def read_nm_config(file_path=None):
    # import pdb
    # pdb.set_trace()
    # file_path = os.path.join(os.getcwd(), file_path)
    if file_path:
        if _is_file_readable(file_path):
            with open(file_path, 'r') as f:
                r = f.read()
                return r
        else:
            return None
    else:
        try:
            # Use 'NM --print-config' to read the configurationo so
            # that the main configuration file and other files in
            # various directories get merged in the right way.
            r = run(['NetworkManager', '--print-config'], split=False)['stdout']
            return r
        except (OSError, CalledProcessError) as e:
            api.current_logger().warning('Error reading NetworkManager configuration: {}'.format(e))
            return None


def parser_nm_config(cfg):
    parser = ConfigParser()

    try:
        if hasattr(parser, 'read_string'):
            # Python 3
            parser.read_string(cfg)
        else:
            # Python 2
            from cStringIO import StringIO
            parser.readfp(StringIO(cfg))
        return parser
    except ParsingError as e:
        api.current_logger().warning('Error parsing NetworkManager configuration: {}'.format(e))
        return None


def check_nm_dchp(nm_cfg, parser):
    if parser.has_option('main', 'dhcp'):
        nm_cfg.dhcp = parser.get("main", "dhcp")
