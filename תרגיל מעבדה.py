#Imports of the relevant packages
import numpy as np
import heapq
from pylab import plot, show, bar
import matplotlib.pyplot as plt
import random

#Event class
class Event():
    def __init__(self, time, eventType, customer=None):
        self.time = time  # event time
        self.eventType = eventType  # Type of the event
        self.customer = customer
        heapq.heappush(P, self)  # add the event to the events list

    def __lt__(self, event2):
        return self.time < event2.time

#Customer class
class Customer():
    def __init__(self, arrival_time, i, type=1):
        self.id = i
        self.arrival_time = arrival_time
        self.type = type  # 1 = regular, 2 = Amnon type
        self.round = 0

# Global variables for generic code
T_max = 14 # 14 work hours each day
NUMOFDAYS = 1 # Number of the needed iterations
P = [] # Minimum tree of the events
R_avg = {i : [] for i in range(7,21)} # Dictionary for analysis of rounds
L_avg = {i : [] for i in range(7,21)} # Dictionary for analysis of L tilda
cust_count = 1 # Total number of customers of naming them
events_lst = ["arriving", "leaving", "arguing", "making a round", "taking a numa"]


for i in range(NUMOFDAYS):
    N = 0 # Number of the arriving customers
    A = 0 # The state of the servers: 0 - Both Anatoly and Nissim are available, 1 - Anatoly or Nissim is busy, 2 - Both of them are busy
    L = 0 # Number of customers in the system
    L_q = 0 # Number of the customers in queue
    L_tilda = 0 # For analysis of average num of customers
    people_in = [] # List of the people in the system
    T_now = 7
    T_prev = 0
    cust_count += 1
    x = np.random.exponential(1 / 20) + 7  # 20 customers per hour means there is a customer every 3 minutes
    t = np.random.random(1)
    if t <= 0.8:
        customer = Customer(x, cust_count)
    else:
        customer = Customer(x, cust_count, 2)
    Event(x, events_lst[0], customer)

    while T_now < T_max + 7 and P:
        event = heapq.heappop(P)
        c = event.customer
        T_prev = T_now
        T_now = event.time
        L_tilda += L*(T_now - T_prev)

        if event.eventType == "arriving":
            print("Customer no. %d arrived at %s" %(c.id, str(T_now)))
            people_in.append(c)
            N += 1
            L += 1
            if L_q >= 5:
                c.round += 1
                if c.round < 2:
                    Event(T_now + (5/60), events_lst[3], c)
            else:
                if A < 2:
                    A += 1
                    if c.type == 2:
                        Event(T_now + (2/60), events_lst[2], c)
                    else:
                        Event(T_now + np.random.exponential(1/20), events_lst[1], c)
                else:
                    L_q += 1

                if T_now <= 20:
                    cust_count += 1
                    if 7 <= T_now < 16:
                        x = np.random.exponential(1 / 20)
                    else:
                        x = np.random.exponential(1/40)
                    t = np.random.random(1)
                    if t <= 0.8:
                        customer2 = Customer(x, cust_count)
                    else:
                        customer2 = Customer(x, cust_count, 2)
                    Event(T_now + x, events_lst[0], customer2)

        elif event.eventType == "leaving":
            print("Customer no. %d left at %s" % (c.id, str(T_now)))
            n = 0
            if c.type == 2:
                n = np.random.random(1)
            if n > 0.85:
                Event(T_now + (20 / 60), events_lst[4])
            else:
                L -= 1
                if L_q == 0:
                    A -= 1
                else:
                    c = people_in.pop(0)
                    L_q -= 1
                    if c.type == 2:
                        Event(T_now + (2 / 60), events_lst[2], c)
                    else:
                        Event(T_now + np.random.exponential(1 / 20), events_lst[1], c)

        elif event.eventType == "making a round":
            print("Customer no. %d making a round at %s" % (c.id, str(T_now)))
            if c.round < 2:
                if L_q < 5:
                    if A < 2:
                        if c.type == 2:
                            Event(T_now + (2 / 60), events_lst[2], c)
                        else:
                            Event(T_now + np.random.exponential(1 / 20), events_lst[1], c)
                    else:
                        L_q += 1
                else:
                    c.round += 1
                    Event(T_now + (5/60), events_lst[3], c)
            else:
                people_in.pop(0)
                L -= 1

        elif event.eventType == "arguing":
            print("Customer no. %d is arguing at %s" % (c.id, str(T_now)))
            Event(T_now + np.random.exponential(1/20), events_lst[1], c)

        elif event.eventType == "taking a numa":
            p = np.random.random(1)
            if p <= 0.5:
                print("Anatoly is taking numa")
            else:
                print("Nissim is taking a numa and dreams about his grandmother")
            if people_in:
                c = people_in[0]
                if c.type == 2:
                    Event(T_now + (2/60), "arguing", c)
                else:
                    Event(T_now + np.random.exponential(1/20), "leaving", c)
            else:
                A -= 1
    # For analisys

print(L_avg)
print(R_avg)