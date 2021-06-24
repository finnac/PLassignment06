import time
import concurrent.futures
import threading

# The Product class, PS5 with ID
class PS5:
  def __init__(self, id):
    self.ID = id
  
  def GetID(self):
    return self.ID

# The Producer class. Has name and the time it takes to produce 1 product,
# also assigns product ID everytime one is produced
class Producer:
  def __init__(self, name, t):
    self.Name = name
    self.Time = t
    self.ProductCount = 1
  
  def Produce(self, ItemQueue):
    # Keep creating products at a given time interval then put it into the ItemQueue
    while(True):
      #ItemQueue.producer_lock.acquire()
      ProductID = self.Name[-2:] + str(self.ProductCount) 
      P = PS5(ProductID)
      print("{0} produced a PS5 with ID: {1}\n".format(self.Name,P.GetID()))
      self.ProductCount += 1
      ItemQueue.PutItem(P)
      #ItemQueue.consumer_lock.release()
      time.sleep(self.Time)
      

# The Consumer class. Has name and the time it takes to consume 1 product
class Consumer:
  def __init__(self, name, t):
    self.Name = name
    self.Time = t

  def Consume(self, ItemQueue):
    # Keep taking products in the ItemQueue at a given time interval 
    # as long as it's not empty
    while(True):
      #ItemQueue.consumer_lock.acquire()     
      PS5 = ItemQueue.TakeItem()
      if PS5 is not None:
        print("{0} purchased a PS5 with ID: {1}\n".format(self.Name,PS5.GetID()))
      #ItemQueue.producer_lock.release()
      time.sleep(self.Time)
      
      
      
# Item Queue Class. Has a stack of item, number of items
class ItemsQueue:
  def __init__(self):
    self.items = []
    self.count = 0
    #self.producer_lock = threading.Lock()
    #self.consumer_lock = threading.Lock()
    #self.consumer_lock.acquire()
  
  # Put item on top of the stack
  def PutItem(self,PS5):
    self.items += [PS5]
    self.count += 1

  # Take item at the top of the stack only when it's not empty
  def TakeItem(self):
    if self.count >= 1:
      Item = self.items[self.count-1]
      self.items.pop(self.count-1)
      self.count -= 1
      return Item



# MAIN--------------------------------------------------------------------------

Q = ItemsQueue()
JP = Producer("SONY JP",0.5)
US = Producer("SONY US",0.5)
A = Consumer("AMAZON",1)
B = Consumer("BESTBUY",1.5)
W = Consumer("WALMART",2)



with concurrent.futures.ThreadPoolExecutor() as executor:#
  #Producer threads
  p1 = executor.submit(JP.Produce,Q)
  p2 = executor.submit(US.Produce,Q)

  #Consumer threads
  c1 = executor.submit(A.Consume,Q)
  c2 = executor.submit(B.Consume,Q)
  c3 = executor.submit(W.Consume,Q)
 