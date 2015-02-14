from bj import *
from physical import physical_up, physical_down
from datalink import MacHeader, encode_mac_header

if __name__ == "__main__":
  bj_layer = BJ(physical_down, physical_up)
  stack = BJ_Stack([bj_layer])

  print(stack.ascend(stack.descend("what a pal")))

  mac_header_obj = MacHeader('A', 'B', "NETWORK", "HERESOMEDATA")
  print(encode_mac_header(mac_header_obj))
