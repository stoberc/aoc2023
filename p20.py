# warning: not generalizable--basically manually tuned to my input,
# which fortunately (and probably generally) has periodic properties

from collections import deque
from math import lcm

FNAME = "in20.txt"

# a flip flop has an internal state, which defaults to off
# whenever an input (several are possible) goes low,
# the internal state is inverted   
class Flip_Flop:

    def __init__(self, name, out_signals):
        
        self.name = name
        self.in_states = {} # not needed, but may help w/ debug
        self.out_signals = out_signals
        self.on = False
        
    # don't actually need this, but useful for debug
    def add_input(self, in_signal):
        self.in_states[in_signal] = False
        
    # receive an input pulse
    def pulse(self, in_signal, value):
        self.in_states[in_signal] = value
        if not value: # low pulse
            self.on = not self.on # triggers state inversion
            for out_signal in self.out_signals: # which cascades to outputs
                pulseQ.append((self.name, out_signal, self.on))

# this is an AND gate w/ active low output
class Conjunction:
    
    def __init__(self, name, out_signals):
    
        self.name = name
        
        # we'll keep track of the number of high inputs
        # marginal speedup probably not necessary since number of inputs
        # to any particular AND appear to be small, but :shrug:
        self.in_states = {}
        self.active_input_count = 0
            
        self.out_signals = out_signals
        self.on = True
            
    # all inputs must be registered in advance
    def add_input(self, in_signal):
        self.in_states[in_signal] = False
        
    # receive an input signal from another component
    def pulse(self, in_signal, value):
        
        # update the number of active inputs
        if self.in_states[in_signal] != value:
            self.in_states[in_signal] = value
            if value:
                self.active_input_count += 1
            else:
                self.active_input_count -= 1
                
        # if all inputs are high, the output goes low
        if self.active_input_count == len(self.in_states):
            out_pulse = False
        else:
            out_pulse = True
            
        # in any case, output pulses are transmitted
        for out_signal in self.out_signals:    
            pulseQ.append((self.name, out_signal, out_pulse)) 

# lone source of signals connected to a button
# broadcaster just passes on whatever it receives from button (always LOW)
class Broadcaster:

    def __init__(self, name, out_signals):
        assert name == 'broadcaster'
        self.name = name
        self.out_signals = out_signals
        
    def pulse(self, name, value):
        assert name == 'button'
        assert value == False
        
        for out_signal in self.out_signals:
            pulseQ.append((self.name, out_signal, value))
        
# read through the input, creating components as described
# defer input wirings until later, 
# since those aren't known until all components have been seen
lines = open(FNAME).read().splitlines()
components = {}
input_wirings = []
for line in lines:
    
    name, outputs = line.split(" -> ")
    outputs = outputs.split(", ")
    
    if name[0] == '%':
        name = name[1:]
        components[name] = Flip_Flop(name, outputs)
          
    elif name[0] == '&':
        name = name[1:]
        components[name] = Conjunction(name, outputs)
        
    else:
        assert name == "broadcaster"
        components[name] = Broadcaster(name, outputs)
        
    for output in outputs:
        input_wirings.append((name, output))
        
# now that we've seen all components and their outputs, we can assign inputs
for in_signal, out_signal in input_wirings:
    # it seems there's a single receive signal that is not actually a component
    if out_signal == 'rx':
        primary_output = in_signal
    else:
        components[out_signal].add_input(in_signal)
    
pulseQ = deque()
low_pulse_count = 0
high_pulse_count = 0

# for Part 2, we're extrapolating when the output signal rx goes low
# manual inspection reveals that the output is an AND gate w/ four input
# signals. If we track these four input signals and pray for periodicity,
# we can extrapolate when all four signals will simultaenously be high.
# Luckily, all four inputs turn out to be periodic (coprime periods),
# w/ zero offset, so extrapolating turns out to be a matter of multiplying all
# four periods together.
press_count = 0
dc_high_times = []
rv_high_times = []
vp_high_times = []
cq_high_times = []
def press_button():
    global low_pulse_count, high_pulse_count, press_count
    press_count += 1
    pulseQ.append(('button', 'broadcaster', False))
    while pulseQ:
        in_signal, out_signal, value = pulseQ.popleft()
        if out_signal != 'rx':
            components[out_signal].pulse(in_signal, value)
            # track the times when the key Part 2 signals go HIGH
            if (in_signal, out_signal, value) == ('dc', 'ns', True):
                dc_high_times.append(press_count)
                #print("dc:", dc_high_times)
            if (in_signal, out_signal, value) == ('rv', 'ns', True):
                rv_high_times.append(press_count)
                #print("rv:", rv_high_times)
            if (in_signal, out_signal, value) == ('vp', 'ns', True):
                vp_high_times.append(press_count)
                #print("vp:", vp_high_times)
            if (in_signal, out_signal, value) == ('cq', 'ns', True):
                cq_high_times.append(press_count)
                #print("cq:", cq_high_times)
        
        # for Part 1
        if value:
            high_pulse_count += 1
        else:
            low_pulse_count += 1
    
# Part 1
for _ in range(1000):
    press_button()
    
print("Part 1:", high_pulse_count * low_pulse_count)

# Part 2, empirically determined sufficient time to witness periodic properties
for _ in range(19000):
    press_button()

#print("dc:", dc_high_times)
#print("rv:", rv_high_times)
#print("vp:", vp_high_times)
#print("cq:", cq_high_times)

print("Part 2:", lcm(dc_high_times[0], rv_high_times[0], vp_high_times[0], cq_high_times[0]))
