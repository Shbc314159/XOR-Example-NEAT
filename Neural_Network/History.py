class History:
    def __init__(self):
        self.next_innovation_number = 0
        self.next_neuron_id = 0
        self.connections = []
        self.neuron_mutations = {}
        self.connection_mutations = {}

history = History()