class BJ_Stack():
  def __init__(self, bjs):
    self._descend = tuple(bjs)
    bjs.reverse()
    self._ascend = tuple(bjs)

  def ascend(self, message):
    '''
      ascend the stack
    '''
    return self.up_step(self._ascend, message)

  def descend(self, message):
    '''
      descend the stack
    '''
    return self.down_step(self._descend, message)

  def up_step(self, stack, message):
    '''
      port the message up one level
    '''
    if len(stack) == 0:
      return message
    # Call the next step with message as one stack up
    return self.up_step(stack[1:], stack[0].inv(message))

  def down_step(self, stack, message):
    '''
      port the message down one level
    '''
    if len(stack) == 0:
      return message
    # Call the next step with message as one stack up
    return self.down_step(stack[1:], stack[0](message))



class BJ():
  def __init__(self, down_func, up_func):
    self._turn_down = down_func
    self._turn_up = up_func

  def __call__(self, for_what):
      '''
        for_what = the message in its current state
      '''
      return self._turn_down(for_what)

  def inv(self, for_what):
      '''
        for_what = the message in its current state
      '''
      return self._turn_up(for_what)

if __name__ == "__main__":
    '''
      main function to transmit up/down the stack
    '''
    def forward(argument):
        return argument - 1

    def backward(argument):
        return argument + 1

    bj_layer = BJ(forward, backward)
    stack = BJ_Stack([bj_layer])

    print(stack.ascend(1))
