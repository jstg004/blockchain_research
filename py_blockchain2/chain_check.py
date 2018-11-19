class CheckChain:
    def check_chain():
        try:
            with open('blockchain.json') as infile:
                blockchain_load = json.load(infile)
        except:
            blockchain_load = None

        return blockchain_load