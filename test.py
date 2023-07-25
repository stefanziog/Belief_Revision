from agent import Agent

def test_revision():
    """ Test if revision works (Success postulate)"""
    print("Testing AGM Postulate: Success")
    s1,s2 = False,False
    agent = Agent()
    agent.belief_base.add('p', 90)
    agent.belief_base.add('q', 80)
    agent.belief_base.add('p>>q', 80)
    if len(agent.belief_base.beliefBase.keys()) == 3:
        s1 = True
    
    agent.belief_base.add('~q', 70)

    if len(agent.belief_base.beliefBase.keys()) == 2:
        s2 = True

    if s1 and s2:
        print("Success test was successful! :)")
    
    else:
        print("Success test was unsuccessful! :(")

def test_contraction():
    """ Test if contraction works """
    agent = Agent()
    agent.belief_base.add('p', 80)
    agent.belief_base.add('~q', 70)
    agent.belief_base._contract('~q')
    agent.belief_base._contract('q')

    if len(agent.belief_base.beliefBase.keys()) == 1:
        print("Contraction test was successful! :)")
    else:
        print("Contraction test was unsuccessful! :(")

def test_expansion():
    """ Test if by expanding a belief gets added  """
    s1,s2 = False, False
    agent = Agent()
    if len(agent.belief_base.beliefBase.keys()) == 0:
        s1 = True
    agent.belief_base.expand('p', 50)
    if len(agent.belief_base.beliefBase.keys()) == 1:
        s2 = True
    
    if s1 and s2:
        print("TEST:Expansion test was successful! :)")
    
    else:
        print("TEST:Expansion test was unsuccessful! :(")

def test_vacuity():
    """ Test contracting a belief that doesn't exist -> Nothing happens """
    s1,s2 = False,False
    agent = Agent()
    agent.belief_base.add('p', 50)
    agent.belief_base.add('q', 55)
    agent.belief_base.add('p>>q', 60)
    if len(agent.belief_base.beliefBase.keys()) == 3:
        s1 = True
    agent.belief_base._contract('r')
    if len(agent.belief_base.beliefBase.keys()) == 3:
        s2 = True

    if s1 and s2:
        print("TEST:Vacuity test was successful! :)")
    else:
        print("TEST:Vacuity test was unsuccessful! :(")

def test_extensionality():
    """ Test resolution """
    agent = Agent()
    agent.belief_base.add('p', 80)
    agent.belief_base.add('q', 90)
    agent.belief_base.add('q<>p', 80)
    if agent.belief_base.entailment('(p>>q)&(q>>p)') == True:
        print("TEST:Extensionality test was successful! :)")
    else:
         print("TEST:Extensionality test was unsuccessful! :(")

def test_consistency():
    """ Test consistency """
    s1,s2,s3 = False,False,False

    agent = Agent()
    agent.belief_base.add('p', 50)
    agent.belief_base.add('q', 40)
    agent.belief_base.add('(p&q)>>r', 30)
    agent.belief_base.add('~r', 38)
    if len(agent.belief_base.beliefBase.keys()) == 1:
        s1 = True

    agent.belief_base.clear()
    agent.belief_base.add('p', 70)
    agent.belief_base.add('~p', 80)
    if len(agent.belief_base.beliefBase.keys()) == 1:
        s2 = True

    agent.belief_base.clear()
    agent.belief_base.add('(p|q)&(p&q)', 97)
    agent.belief_base.add('~p', 56)
    if len(agent.belief_base.beliefBase.keys()) == 1:
        s3 = True

    if s1 and s2 and s3:
        print("TEST:Consistency test successful! :)")
    else:
        print("TEST:Consistency test unsuccessful! :(")

test_revision()
test_vacuity()
test_contraction()
test_expansion()
test_extensionality()
test_consistency()
