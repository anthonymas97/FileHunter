from fiinder_1 import Search
from time import sleep

if __name__ == "__main__":
    #startSearch()
    #sleep(10)
    search = Search()
    #sleep(35)
    items = search.search('trademark')
    print('TOTAL LIST: ', items)
