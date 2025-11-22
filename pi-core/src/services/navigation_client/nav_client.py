class NavClient:
    """
    Client gửi/nhận toạ độ tới phone/back-end.
    Hiện tại để stub, sau này nối với backend hoặc Maps trên phone.
    """

    def __init__(self, event_bus, network_cfg):
        self.event_bus = event_bus
        self.network_cfg = network_cfg

    async def send_nav_command(self, target_place):
        pass
