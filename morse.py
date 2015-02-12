from bj import *
from physical import physical_up, physical_down

if __name__ == "__main__":
  bj_layer = BJ(physical_down, physical_up)
  stack = BJ_Stack([bj_layer])
 
  print(stack.ascend(stack.descend("what a pal")))
