import yaml
import grpc

from google.protobuf.json_format import MessageToDict

from ipnet.examples.bgp.gobgp.proto import gobgp_pb2
from ipnet.examples.bgp.gobgp.proto import gobgp_pb2_grpc


class GoBGPAPIClient:

    def __init__(self, gobgp_ip, gobgp_port):
        """Constructor initialises RPC session

        Args:
            target_ipv4_address: Management IPv4 Address of GoBGP instance
            target_rpc_port: Management Port of GoBGP Instance
            connect: When set false, will not build grpc channel or api stub objects
        """
        self.gobgp_ip = gobgp_ip
        self.gobgp_port = gobgp_port
        self.channel = None
        self.gobgp_api_stub = None

    def connect(self):
        self.channel = grpc.insecure_channel(f"{self.gobgp_ip}:{self.gobgp_port}")
        self.gobgp_api_stub = gobgp_pb2_grpc.GobgpApiStub(self.channel)

    def close(self):
        self.channel.close()

    @staticmethod
    def _build_rpc_request() -> gobgp_pb2.ListPathRequest:
        request = gobgp_pb2.ListPathRequest(
            table_type=gobgp_pb2.GLOBAL,
            name="",
            family=gobgp_pb2.Family(afi=gobgp_pb2.Family.AFI_LS, safi=gobgp_pb2.Family.SAFI_LS),
            prefixes=None,
            sort_type=True,
        )
        return request

    def get_bgp_ls_table(self) -> list:
        request = self._build_rpc_request()
        response = self.gobgp_api_stub.ListPath(request)
        rtn = [MessageToDict(nlri) for nlri in response]
        return rtn
