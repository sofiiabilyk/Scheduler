'''
__init__(self):
left(self, i):
right(self, i):
def parent(self, i):
def heappush(self, key):
def heapify(self, i):
def heappop(self):
'''
class MaxHeapq:
    """ 
    A class that implements properties and methods 
		that support a max priority queue data structure

		Attributes
	  ----------
	  heap : arr
	      A Python list where key values in the max heap are stored
	  heap_size: int
	      An integer counter of the number of keys present in the max heap
	  """  

    def __init__(self):    
        """
        Parameters
        ----------
        None
        """    
        self.heap       = []
        self.heap_size  = 0
        
    def left(self, i):
        """
        Takes the index of the parent node
        and returns the index of the left child node

        Parameters
        ----------
        i: int
          Index of parent node

        Returns
        ----------
        int
          Index of the left child node
        """
        return 2 * i + 1

    def right(self, i):
        """
        Takes the index of the parent node
        and returns the index of the right child node
        
        Parameters
        ----------
        i: int
            Index of parent node

        Returns
        ----------
        int
            Index of the right child node
        """
        return 2 * i + 2
		
    def parent(self, i):
        """
        Takes the index of the child node
        and returns the index of the parent node
        
        Parameters
        ----------
        i: int
            Index of child node

        Returns
        ----------
        int
            Index of the parent node
        """

        return (i - 1)//2

    def maxk(self):     
        """
        Returns the highest key in the priority queue. 
        
        Parameters
        ----------
        None

        Returns
        ----------
        int
            the highest key in the priority queue
        """
        return self.heap[0]         
  
    def heappush(self, key):  
        """
        Insert a key into a priority queue 
        
        Parameters
        ----------
        key: int
            The key value to be inserted

        Returns
        ----------
        None
        """
        # insert -inf, as it is guaranteed to be smaller than all other 
        # elements -> should be located in the end
        # to not break the max-heap property
        self.heap.append(-float("inf")) 
        self.increase_key(self.heap_size,key)
        self.heap_size+=1
        
    def increase_key(self, i, key): 
        """
        Modifies the value of a key in a max priority queue
        with a higher value
        
        Parameters
        ----------
        i: int
            The index of the key to be modified
        key: int
            The new key value

        Returns
        ----------
        None
        """
        if key < self.heap[i]:
            raise ValueError('new key is smaller than the current key')
        self.heap[i] = key
        # if the parent is smalle we should swap the elements 
        # to not break the max-heap property
        while i > 0 and self.heap[self.parent(i)] < self.heap[i]:
            j = self.parent(i)
            holder = self.heap[j]
            self.heap[j] = self.heap[i]
            self.heap[i] = holder
            i = j    
       
    def heapify(self, i):
        """
        Creates a max heap from the index given
        
        Parameters
        ----------
        i: int
            The index of the root node of the subtree to be heapify

        Returns
        ----------
        None
        """
        l = self.left(i)
        r = self.right(i)
        heap = self.heap
        #looking for the largest value among 
        # parent, right & left children 
        # to make the largest a parent
        if l <= (self.heap_size-1) and heap[l]>heap[i]:
            largest = l
        else:
            largest = i
        if r <= (self.heap_size-1) and heap[r] > heap[largest]:
            largest = r
        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            self.heapify(largest)

    def heappop(self):
        """
        returns the larest key in the max priority queue
        and remove it from the max priority queue
        
        Parameters
        ----------
        None

        Returns
        ----------
        int
            the max value in the heap that is extracted
        """
        if self.heap_size < 1:
            raise ValueError('Heap underflow: There are no keys in the priority queue ')
        maxk = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heap_size-=1
        self.heapify(0)
        return maxk

    def remove(self, key):
        """
        Removes the specified key from the max heap

        Parameters
        ----------
        key: int
            The key value to be removed

        Returns
        ----------
        None
        """
        try:
            index = self.heap.index(key)
        except ValueError:
            raise ValueError("Key not found in heap")

        # Replace with last element and heap
        self.heap[index] = self.heap[-1]
        self.heap.pop()
        self.heap_size -= 1

        # Restore heap property
        if index < self.heap_size:
            parent_index = self.parent(index)
            if index > 0 and self.heap[index] > self.heap[parent_index]:
                self.increase_key(index, self.heap[index])
            else:
                self.heapify(index)

def test_maxheapq():

    """
        Tests the class MaxHeapq

        Parameters
        ----------
        None

        Returns
        ----------
        None
    """

    print("Running test cases...")

    print("Test 1: Basic insertion and max retrieval")
    h = MaxHeapq()
    h.heappush(10)
    h.heappush(20)
    h.heappush(5)
    print(h.maxk() == 20)
    
    print("Test 2: Pop max and check heap property")
    print(h.heappop() == 20)
    print(h.maxk() ==  10)

    print("Test 3: pudh more values in and remove the key")
    h.heappush(17)
    h.heappush(23)
    h.heappush(4)
    print(h.heap)
    h.remove(23)
    print(h.heap)  # Should not contain 10


    print("All tests passed!")




#test_maxheapq()

    