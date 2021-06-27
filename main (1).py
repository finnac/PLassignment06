#Group 7

import time
import concurrent.futures

# The Product class, PS5 with ID
class PS5:
  def __init__(self, id):
    self.ID = id


# Item Queue Class: a stack structuce, last in - first out basis 
# Has list of items, number of items and max capacity
class ItemsQueue:
  def __init__(self, Max):
    self.items = []
    self.count = 0
    self.max = Max
  
  # Put item on top of the stack
  def PutItem(self,PS5):
    self.items += [PS5]
    self.count += 1

  # Return the item at the top of the stack only when it's not empty
  def TakeItem(self):
    if self.count >= 1:
      self.count -= 1
      return self.items.pop()


# The Producer class. Has name and the time it takes to produce 1 product,
# also assigns product ID everytime one is produced
class Producer:
  def __init__(self, name, t):
    self.Name = name
    self.Time = t
    self.ProductCount = 1
  
  def Produce(self, ItemQueue):
    # Keep creating products at a given time interval then put it into the ItemQueue
    # as long as there is still space in Queue
    while(True):
      if ItemQueue.count < ItemQueue.max:
        # Process product ID
        ProductID = self.Name[-2:] + str(self.ProductCount) 
        P = PS5(ProductID)
        # Produce Item and put in Queue
        print("[{0}] produced a PS5 with ID: {1}\n".format(self.Name,P.ID))
        self.ProductCount += 1
        ItemQueue.PutItem(P)
        time.sleep(self.Time)
      

# The Consumer class. Has name and the time it takes to consume 1 product
class Consumer:
  def __init__(self, name, t):
    self.Name = name
    self.Time = t

  def Consume(self, ItemQueue):
    # Keep taking products from the ItemQueue at a given time interval 
    while(True):   
      PS5 = ItemQueue.TakeItem()
      if PS5 is not None:
        print("-{0}- purchased a PS5 with ID: {1}\n".format(self.Name,PS5.ID))
      time.sleep(self.Time)

# MAIN--------------------------------------------------------------------------

#Queue with max capacity of 25 products
Q = ItemsQueue(25)

#Producers
JP = Producer("SONY JP", 0.5)
US = Producer("SONY US", 0.5)

#Consumers
A = Consumer("AMAZON", 1)
B = Consumer("BESTBUY", 1.5)
W = Consumer("WALMART", 1)


with concurrent.futures.ThreadPoolExecutor() as executor:
  #Producer threads
  p1 = executor.submit(JP.Produce,Q)
  p2 = executor.submit(US.Produce,Q)

  #Consumer threads
  c1 = executor.submit(A.Consume,Q)
  c2 = executor.submit(B.Consume,Q)
  c3 = executor.submit(W.Consume,Q)
 