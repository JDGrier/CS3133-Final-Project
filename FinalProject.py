
def createDFA(substring):
    dfa = {}
    n = len(substring)

    for i in range(n):
        dfa[i] = {}

    trap_state = n
    dfa[trap_state] = {0: trap_state, 1: trap_state}


    for i in range(n):
        if substring[i] == '0':
            dfa[i][0] = i + 1 if i + 1 < n else trap_state
        else:
            dfa[i][0] = 1 if substring[0] == '0' else 0
        if substring[i] == '1':
            dfa[i][1] = i + 1 if i + 1 < n else trap_state
        else:
            dfa[i][1] = 1 if substring[0] == '1' else 0

    dfa[n] = {0: n, 1: n}

    return dfa


def createGNFA(DFA, start_state, accept_states):
    gnfa = {}
    l = len(DFA)
    trapState = l - 1
    # l - 1 because the trap state is not needed in the gnfa.
    for i in range(trapState):
        gnfa[i] = DFA[i]

    # Step 1: Add a new start state to the GNFA with an epsilon transition to the original DFA start state
    gnfa["start"] = {"ε": start_state}  # ε transition to the original start state

    # Step 2: Add a new end state with epsilon transitions from all original accept states
    for accept_state in accept_states:
      if accept_state in gnfa:
            gnfa[accept_state]["ε"] = "end"


    #dont need transitions to the trap state, check state before trap state and remove the transition
    if gnfa[trapState-1][0] == trapState:
      del gnfa[trapState-1][0]
    if gnfa[trapState-1][1] == trapState:
      del gnfa[trapState-1][1]
    return gnfa


def eliminateStateForExclusion(GNFA, stateToEliminate):
    gnfa = GNFA.copy()

    # Check if there is a self-loop on the state we're eliminating
    self_loop = gnfa[stateToEliminate].pop(stateToEliminate, None)

    transitions_to_update = {}  # Store updates as a dictionary of (incoming_state -> outgoing_state)

    # Handle transitions from other states to the state we're eliminating
    for incoming_state in gnfa:
        if stateToEliminate in gnfa[incoming_state]:
            transition_to_eliminate = gnfa[incoming_state].pop(stateToEliminate)

            # Combine transitions from the eliminated state to other states
            for outgoing_transition, outgoing_state in gnfa[stateToEliminate].items():
                combined_transition = str(transition_to_eliminate)

                # Add the Kleene star if there is a self-loop
                if self_loop is not None:
                    combined_transition += f"({str(self_loop)})*"

                # Avoid unnecessary ε transitions
                if outgoing_transition == 'ε':
                    combined_transition = combined_transition.replace('ε', '')
                    
                combined_transition += f"({str(outgoing_transition)})" if outgoing_transition != 'ε' else ""


                # Union the transitions if there are multiple transitions to the same state
                if (incoming_state, outgoing_state) in transitions_to_update:
                    transitions_to_update[(incoming_state, outgoing_state)] = (
                        f"({transitions_to_update[(incoming_state, outgoing_state)]})U({combined_transition})"
                    )
                else:
                    transitions_to_update[(incoming_state, outgoing_state)] = combined_transition

    # Apply the updates to the GNFA
    for (incoming_state, outgoing_state), new_transition in transitions_to_update.items():
        if outgoing_state == 'end':
            # Combine multiple transitions to the end state using union (U)
            existing_transitions = [key for key in gnfa[incoming_state].keys() if gnfa[incoming_state][key] == 'end']
            if existing_transitions:
                for existing_transition in existing_transitions:
                    # Union the existing transition with the new one
                    new_transition = f"({existing_transition})U({new_transition})"
                    del gnfa[incoming_state][existing_transition]
            gnfa[incoming_state][new_transition] = 'end'
        else:
            if new_transition not in gnfa[incoming_state]:
                gnfa[incoming_state][new_transition] = outgoing_state

    # Special case: when eliminating state 0, update 'start' to transition to 'end'
    if stateToEliminate == 0:
        start_transition = gnfa['start'].get('ε', '')

        # Only apply the Kleene star if the self-loop exists
        kleene_star_loop = f"({self_loop})*" if self_loop is not None else ""

        # Combine the self-loop with all outgoing transitions from state 0
        combined_transitions = []
        for outgoing_transition, outgoing_state in gnfa[stateToEliminate].items():
            # Apply the self-loop (if any) to each outgoing transition
            combined_transition = f"{outgoing_transition}" if outgoing_transition != 'ε' else ''
            combined_transitions.append(combined_transition)

        # Union the outgoing transitions, grouping them properly and keeping the self-loop outside the union
        if combined_transitions:
            final_combined_transition = f"{kleene_star_loop}({')U('.join(combined_transitions)})"
        else:
            final_combined_transition = kleene_star_loop

        # Include the start state's ε-transition if present, and group it with the other transitions
        if start_transition:
            if start_transition != 'ε':
                final_combined_transition = f"{kleene_star_loop}({start_transition}U({final_combined_transition}))"
            else:
                final_combined_transition = f"{kleene_star_loop}({final_combined_transition})"

        # Set the final transition from 'start' to 'end'
        gnfa['start'] = {final_combined_transition: 'end'}

    # Finally, remove the eliminated state
    del gnfa[stateToEliminate]

    return gnfa

def reduceGNFA(GNFA):
    stateToEliminate = len(GNFA) - 2
    gnfa = GNFA
    if stateToEliminate >= 0:
        gnfa = eliminateStateForExclusion(GNFA, stateToEliminate)
        gnfa = reduceGNFA(gnfa)
    return gnfa
# Example DFA and GNFA creation:
dfa = createDFA("01")
# Define accepting states: all states except the last one are accepting
accepting_states = set(range(len(dfa) - 1))

# Convert DFA to GNFA with proper accepting states
gnfa = createGNFA(dfa, 0, accepting_states)


finalGNFA = reduceGNFA(gnfa)

regExpression = ""
for transition, state in finalGNFA['start'].items():
    if(state == 'end'):
        regExpression = transition

print(regExpression)

