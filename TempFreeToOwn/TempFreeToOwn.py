from pysteamkit.steam3.client import SteamClient

class SimpleCallBack:
    def handle_message(self, emsg_real, body):
        pass
    def try_initialize_connection(self, *args, **kwargs):
        return True

client = SteamClient(SimpleCallBack())
client.initialize()
client.login_anonymous()

print "Response:", client.steamapps.get_product_info(apps=(620,))
print "\n\n"

