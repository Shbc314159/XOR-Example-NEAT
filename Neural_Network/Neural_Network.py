from . import Genome
from . import History

history = History.history

import random
import copy
from line_profiler import LineProfiler
from numba import njit
import pickle

class Neural_Network:
    try:
        from line_profiler import profile
    except ImportError:
        def profile(func):
            return func
    def __init__(self, num_inputs, num_outputs, mutate_neuron_prob, mutate_connection_prob, mutate_weight_prob):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.genome = Genome.Genome()
        self.setup()
        self.fitness = 0
        self.mutate_neuron_prob = mutate_neuron_prob
        self.mutate_connection_prob = mutate_connection_prob
        self.mutate_weight_prob = mutate_weight_prob
        self.rebuild = True
    
    @classmethod
    def empty(cls, num_inputs, num_outputs, mutate_neuron_prob, mutate_connection_prob, mutate_weight_prob):
        self = object.__new__(cls)
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.genome = Genome.Genome()
        self.empty_setup()
        self.fitness = 0
        self.mutate_neuron_prob = mutate_neuron_prob
        self.mutate_connection_prob = mutate_connection_prob
        self.mutate_weight_prob = mutate_weight_prob
        self.rebuild = False
        return self

    def setup(self):
        for i in range(self.num_inputs):
            self.genome.add_neuron('input', i)
        
        for i in range(self.num_outputs):
            self.genome.add_neuron('output', i+self.num_inputs)
        
        self.genome.add_neuron('bias', self.num_inputs+self.num_outputs)

        for input_neuron in self.genome.neurons.values():
            if input_neuron.type in ['input', 'bias']:
                for output_neuron in self.genome.neurons.values():
                    if output_neuron.type == 'output':
                        self.add_connection(input_neuron.id, output_neuron.id)
    
        if History.history.next_neuron_id == 0:
            History.history.next_neuron_id = self.num_inputs + self.num_outputs + 1
    
    def empty_setup(self):
        for i in range(self.num_inputs):
            self.genome.add_neuron('input', i)
        
        for i in range(self.num_outputs):
            self.genome.add_neuron('output', i+self.num_inputs)
        
        self.genome.add_neuron('bias', self.num_inputs+self.num_outputs)
    
    def add_connection(self, input_neuron, output_neuron):

        if self._would_create_cycle(input_neuron, output_neuron):
            return None

        new_mutation = (input_neuron, output_neuron)
        if new_mutation in history.connection_mutations:
            innovation_num = history.connection_mutations[new_mutation]
            if innovation_num not in self.genome.connections:
                conn = self.genome.add_connection(input_neuron, output_neuron, innovation_num)
                self.rebuild = True
                return conn

        else:
            innovation_num = history.next_innovation_number
            history.next_innovation_number += 1
            history.connection_mutations[new_mutation] = innovation_num
            conn = self.genome.add_connection(input_neuron, output_neuron, innovation_num)
            self.rebuild = True
            return conn

    
    def add_neuron(self, connection):
        neuron_in = connection.input_neuron
        neuron_out = connection.output_neuron

        num = connection.innovation_number
        if num in history.connection_mutations:
            neuron_id = history.neuron_mutations[num]

            if neuron_id not in self.genome.neurons:
                self.genome.add_neuron('hidden', neuron_id)
                conn1 = self.add_connection(neuron_in, neuron_id)
                conn2 = self.add_connection(neuron_id, neuron_out)
            
        else:
            neuron_id = history.next_neuron_id
            history.next_neuron_id += 1
            history.neuron_mutations[num] = neuron_id
            self.genome.add_neuron('hidden', neuron_id)
            conn1 = self.add_connection(neuron_in, neuron_id)
            conn2 = self.add_connection(neuron_id, neuron_out)

        if conn1 and conn2:
            return conn1 and conn2
        
        return None
        
    def reset(self):
        for neuron in self.genome.neurons.values():
            neuron.reset()
    
    def mutate_connection(self):
        # pull local refs
        neurons = list(self.genome.neurons.values())
        rand_choice = random.choice

        # pick an input neuron once from non‐outputs
        non_outputs = [n for n in neurons if n.type != 'output']
        if not non_outputs:
            return
        input_neuron = rand_choice(non_outputs)

        # pick an output neuron once from valid targets
        valid_outputs = [
            n for n in neurons
            if n.type not in ('input', 'bias')
               and n.id != input_neuron.id
        ]
        if not valid_outputs:
            return
        output_neuron = rand_choice(valid_outputs)

        # add the new connection
        self.add_connection(input_neuron.id, output_neuron.id)


    def mutate_neuron(self):
        conn = random.choice([c for c in self.genome.connections.values()])
        self.add_neuron(conn)


    def mutate_weights(self):
        # cache random helpers
        rand = random.random
        gauss = random.gauss
        uniform = random.uniform

        # one‐off threshold check
        if rand() >= self.mutate_weight_prob:
            return

        small_p = 0.1
        # pull out dict values once
        for conn in self.genome.connections.values():
            if rand() < small_p:
                # full re‐initialization
                conn.weight = uniform(-1.0, 1.0)
            else:
                # small Gaussian tweak
                conn.weight += gauss(0, 0.05)


    @profile
    def mutate(self):
        # cache locals
        rand = random.random
        conn_p = self.mutate_connection_prob
        neur_p = self.mutate_neuron_prob

        # maybe add a connection
        if rand() < conn_p:
            self.mutate_connection()

        # maybe split a neuron
        if rand() < neur_p and self.genome.connections:
            self.mutate_neuron()

        # mutate weights in one pass
        self.mutate_weights()

    @profile       
    def crossover(self, other):
        cs = self.genome.connections
        co = other.genome.connections
        fit_s, fit_o = self.fitness, other.fitness

        keys_s = set(cs)
        keys_o = set(co)

        common = keys_s & keys_o
        disj_s = keys_s - keys_o
        disj_o = keys_o - keys_s

        child = Neural_Network.empty(self.num_inputs, self.num_outputs, self.mutate_neuron_prob, self.mutate_connection_prob, self.mutate_weight_prob)
        child_conn = {}

        for k in common:
            child_conn[k] = cs[k].clone()

        if fit_s <= fit_o:
            for k in disj_o:
                child_conn[k] = co[k].clone()
        else:
            for k in disj_s:
                child_conn[k] = cs[k].clone()

        child.genome.connections = child_conn
        child.genome.add_neurons_from_connections()
        child.rebuild = True
        return child
    
    def rebuild_execution_order(self):
        # 1. Build maps of incoming & outgoing active connections
        incoming = {nid: [] for nid in self.genome.neurons}
        outgoing = {nid: [] for nid in self.genome.neurons}
        for conn in self.genome.connections.values():
            if conn.active:
                incoming[conn.output_neuron].append(conn)
                outgoing[conn.input_neuron].append(conn)

        in_deg = {nid: len(incoming[nid]) for nid in self.genome.neurons}

        queue = [nid for nid, deg in in_deg.items() if deg == 0]
        order = []

        while queue:
            nid = queue.pop(0)
            for conn in outgoing[nid]:
                m = conn.output_neuron
                in_deg[m] -= 1
                if in_deg[m] == 0:
                    queue.append(m)
            
            if self.genome.neurons[nid].type not in ('input', 'bias'):
                order.append(nid)

        self._incoming_map = incoming
        self._exec_order   = order
        self._output_ids   = [
            n.id for n in self.genome.neurons.values()
            if n.type == 'output'
        ]

    def fast_run(self, inputs):
        if self.rebuild:
            self.rebuild_execution_order()
        self.reset()

        for i, v in enumerate(inputs):
            self.genome.neurons[i].value = v
        
        bias_id = self.num_inputs + self.num_outputs
        self.genome.neurons[bias_id].value = 1.0

        for nid in self._exec_order:
            neuron = self.genome.neurons[nid]
            total = 0.0
            for conn in self._incoming_map[nid]:
                if conn.active:
                    total += conn.weight * self.genome.neurons[conn.input_neuron].value
            neuron.sum = total
            neuron.activate()

        return [ self.genome.neurons[nid].value for nid in self._output_ids ]
    
    def _would_create_cycle(self, src_id, dst_id):
        stack = [dst_id]
        visited = set()
        while stack:
            cur = stack.pop()
            if cur == src_id:
                return True
            visited.add(cur)
            # for every outgoing conn from cur
            for conn in self.genome.connections.values():
                if conn.active and conn.input_neuron == cur:
                    nxt = conn.output_neuron
                    if nxt not in visited:
                        stack.append(nxt)
        return False

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"Network saved to {filepath!r}")

    @classmethod
    def load(cls, filepath):
        with open(filepath, 'rb') as f:
            obj = pickle.load(f)
        if not isinstance(obj, cls):
            raise TypeError(f"Loaded object is not a {cls.__name__}")
        print(f"Network loaded from {filepath!r}")
        return obj