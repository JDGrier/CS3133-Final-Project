def createDFA(substring):
    dfa = {}
    l = len(substring)

    for state in range(l):
        dfa[state] = {}

    trapState = l
    dfa[trapState] = {0: trapState, 1: trapState} 

    # building transitions
    for state in range(l):
        if substring[state] == '0':
            nextState = state + 1 if state + 1 < l else trapState
            dfa[state][0] = nextState
        else:
            dfa[state][0] = 1 if substring[0] == '0' else 0
        if substring[state] == '1':
            nextState = state + 1 if state + 1 < l else trapState
            dfa[state][1] = nextState
        else:
            dfa[state][1] = 1 if substring[0] == '1' else 0


    return dfa


def createGNFA(dfa, startState, acceptStates):
    gnfa = {}
    dfaLength = len(dfa)
    trapState = dfaLength - 1
    # dfaLength - 1 because the trap state is not needed in the GNFA.
    for i in range(trapState):
        gnfa[i] = dfa[i]

    # adding an initial state
    gnfa["start"] = {"ε": startState} 

    # adding an epsilon transition to all accept states
    for acceptState in acceptStates:
        if acceptState in gnfa:
            gnfa[acceptState]["ε"] = "end"

    # can remove transitions to trap state
    if gnfa[trapState - 1][0] == trapState:
        del gnfa[trapState - 1][0]
    if gnfa[trapState - 1][1] == trapState:
        del gnfa[trapState - 1][1]
    return gnfa


def eliminateState(gnfa, stateToEliminate):
    gnfa = gnfa.copy()

    # remove and record self-loop if it exists
    selfLoop = gnfa[stateToEliminate].pop(stateToEliminate, None)

    transitionsToUpdate = {}

    for incomingState in gnfa:
        if stateToEliminate in gnfa[incomingState]:
            transitionToEliminate = gnfa[incomingState].pop(stateToEliminate)

            # combine eliminated transitions out into transitions in
            for outgoingTransition, outgoingState in gnfa[stateToEliminate].items():
                combinedTransition = str(transitionToEliminate)

                # add star to record self loops
                if selfLoop is not None:
                    combinedTransition += f"({str(selfLoop)})*"

                # dont record epsilon transitions by themselves
                if outgoingTransition == 'ε':
                    combinedTransition = combinedTransition.replace('ε', '')

                if outgoingTransition != 'ε':
                  combinedTransition += f"({str(outgoingTransition)})"

                # union the transitions if there are multiple transitions to the same state
                if (incomingState, outgoingState) in transitionsToUpdate:
                    transitionsToUpdate[(incomingState, outgoingState)] = (
                        f"({transitionsToUpdate[(incomingState, outgoingState)]})U({combinedTransition})"
                    )
                else:
                    transitionsToUpdate[(incomingState, outgoingState)] = combinedTransition

    for (incomingState, outgoingState), newTransition in transitionsToUpdate.items():
      if outgoingState == 'end':
          existingTransitions = []
          for key in gnfa[incomingState].keys():
              if gnfa[incomingState][key] == 'end':
                  existingTransitions.append(key)
          #combine transitions to end
          if len(existingTransitions) > 0:
              for existingTransition in existingTransitions:
                  newTransition = f"({existingTransition})U({newTransition})"
                  del gnfa[incomingState][existingTransition]
          gnfa[incomingState][newTransition] = 'end'
      else:
          if newTransition not in gnfa[incomingState]:
              gnfa[incomingState][newTransition] = outgoingState

    # when the state being eliminated is 0
    if stateToEliminate == 0:
        startTransition = gnfa['start'].get('ε', '')

        starLoop = f"({selfLoop})*" if selfLoop is not None else ""

        combinedTransitions = []
        for outgoingTransition, outgoingState in gnfa[stateToEliminate].items():
            # apply self loop to existing transitions if exists
            combinedTransition = f"{outgoingTransition}" if outgoingTransition != 'ε' else ''
            combinedTransitions.append(combinedTransition)

        if combinedTransitions:
            finalCombinedTransition = f"{starLoop}({')U('.join(combinedTransitions)})"
        else:
            finalCombinedTransition = starLoop

        finalCombinedTransition = f"{starLoop}({finalCombinedTransition})"

        gnfa['start'] = {finalCombinedTransition: 'end'}

    # remove eliminated state
    del gnfa[stateToEliminate]

    return gnfa


def reduceGNFA(gnfa):
    stateToEliminate = len(gnfa) - 2
    gnfa = gnfa
    if stateToEliminate >= 0:
        gnfa = eliminateState(gnfa, stateToEliminate)
        gnfa = reduceGNFA(gnfa)
    return gnfa


print("Enter a binary string to exlude: ")
s = input()
dfa = createDFA("s")

acceptingStates = set(range(len(dfa) - 1))

gnfa = createGNFA(dfa, 0, acceptingStates)

finalGNFA = reduceGNFA(gnfa)

regExpression = ""

for transition, state in finalGNFA['start'].items():
    if state == 'end':
        regExpression = transition

print(regExpression)
