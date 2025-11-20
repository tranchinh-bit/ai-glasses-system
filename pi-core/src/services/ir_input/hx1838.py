# Stub – sau có thể dùng thư viện RPi.GPIO hoặc pigpio
# để đọc tín hiệu IR từ module HX1838.

class IRRemote:
  def __init__(self, gpio_pin: int = 17):
      self.gpio_pin = gpio_pin

  def start(self):
      # TODO: implement real IR decoding
      pass
