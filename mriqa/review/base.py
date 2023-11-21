from mriqa import config
from mriqa.messages import INPUT_ERR


class reviewer():

    def __init__(self):
        func = config.collector._db
        self.db, self.filename = func()
    

    def check(self):
        func = config.collector._check
        fargs = {'collection': self.db}
        return func(**fargs)
    
    def review(self, img):
        func = config.collector._review
        fargs = {'img': img, 'collection': self.db}
        func(**fargs)

    def artifacts(self):
        func = config.collector._artifacts
        fargs = {'sigma': self.sigma, 'truncate': self.sdlen, 'mode': 'reflect'}

        func(collections = self.db, **fargs)



def list_collections(collections):
    """Generate list of already recorded results """
    from mriqa.review import verify_input

    if not collections:
        print('No sessions to resume, exiting.')
        quit()

    list_ses = ''
    for i, file in enumerate(collections):
        list_ses +=(f'{i+1}. {file}\n')
        
    index = verify_input(question = list_ses, select = "Enter session number to resume: ", 
                        n =collections, err ="Invalid session, try again:\n")
    #print("\033c")
    return collections[int(index)-1]