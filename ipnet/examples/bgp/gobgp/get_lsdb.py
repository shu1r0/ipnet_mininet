import argparse

from ipnet.examples.bgp.gobgp.gobgp_api_client import GoBGPAPIClient


def get_args(description=None):
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--ip', type=str)
    parser.add_argument('--port', type=int)

    args = parser.parse_args()
    return args


def get_lsdb(ip, port) -> list:
    client = GoBGPAPIClient(gobgp_ip=ip, gobgp_port=port)

    client.connect()
    lsdb = client.get_bgp_ls_table()
    client.close()

    return lsdb


if __name__ == '__main__':
    args = get_args()
    lsdb = get_lsdb(args.ip, args.port)
    print(lsdb)
