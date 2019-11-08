# Example implementation for search
#
#

from fiinder_1 import Search
from time import sleep

search = 0

# local subscriber to the new list
# returns full new list and the keyword it was searched against
def newList(list, keyword, finished):
    print('FOUND NEW LIST: ', len(list), '; Keyword: ', keyword, '; FINISHED: ', finished)

if __name__ == "__main__":
    try:
        # instantiate search object
        search = Search()

        # subscribe to the newFileList event to get notified when new results are in
        # because opening and reading files may take time, 
        # this way the UI can be updated as soon as a new file is available
        search.events.newFileList += newList

        # execute a new searches
        # this also returns the final list synchronously if you dont want to use callback
        search.search('trademark')
        search.stopSearch()

    except Exception as e:
        print('ERROR', e)
