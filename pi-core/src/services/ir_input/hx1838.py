class IRRemoteHX1838:
    """
    Stub, tuỳ bạn dùng thư viện nào (lirc, pigpio...).
    Ý tưởng: map một số nút -> hành động:
    - SOS
    - thay đổi profile pin
    - chuyển mode OFFLOAD
    """

    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def run(self):
        # TODO: lắng nghe IR và publish event
        pass
