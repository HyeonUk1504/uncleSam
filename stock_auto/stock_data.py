import datetime
from stockAPI import translate


#주식정보
class Node:
    def __init__(self, name, date_acquired , quantity, cost, currency, en_name = None):
        self.date_acquired = date_acquired
        self.quantity = quantity
        self.cost = cost
        self.name = name
        self.next = None
        self.currency = currency
        self.en_name = en_name
    
#주식 매수정보
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.profit = 0
        self.size = 0

    def is_empty(self):
        if not self.head:
            return True

        return False

    def enqueue(self, name, date_acquired , quantity, cost, currency):
        new_node = Node(name, date_acquired , quantity, cost, currency)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.size += 1
            new_node.en_name = translate(name)
            return

        self.tail.next = new_node
        self.tail = new_node
        self.size += 1
        new_node.en_name = self.head.en_name

    def insert_front(self, node):

        if self.is_empty():
            self.head = node
            self.tail = node
            return
        node.next = self.head
        self.head = node

    def dequeue(self):
        if self.is_empty():
            return None

        ret_Node = self.head
        self.head = self.head.next
        return ret_Node

    def stock_quantity_check(self):
        if self.is_empty():
            return 0
        return self.head.quantity

    def peek_Node(self):
        if self.is_empty():
            return None
        return self.head()

    def check_Node(self):
        if self.is_empty():
            print('empty!!!')
            return

        else:
            stock_left = []
            for i in range(self.size):
                stock_left.append(self.dequeue())
            return stock_left

   # 주식 보유기간 ST or LT 인지 구분하기 위한 함수
def date_difference(date1,date2):
    date1 = str(date1)
    date2 = str(date2)
    sold_time = datetime.date(int(date1[4:]),int(date1[:2]),int(date1[2:4]))
    acquired_time = datetime.date(int(date2[4:]),int(date2[:2]),int(date2[2:4]))
    day_diff = sold_time - acquired_time
    if day_diff.days >= 365 :
        result = 'LT'

    else:
        result = 'ST'

    return result
    



