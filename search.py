from fiinder_1 import Search
from time import sleep

num = 0
search = 0

# local subscriber to the new list
# returns full new list and the keyword it was searched against
def newList(list, keyword):
    global num
    print('FOUND NEW LIST', keyword)

    # example to stop the search
    num += 1
    if num >= 20:
        search.stopSearch()

if __name__ == "__main__":
    try:
        # instantiate search object
        search = Search()

        # subscribe to the newFileList event to get notified when new results are in
        # because opening and reading files may take time, 
        # this way the UI can be updated as soon as a new file is available
        search.events.newFileList += newList

        # execute a new search
        while search.isIndexing():
            continue
        search.search('trademark')

    except Exception as e:
        print('ERROR', e)
