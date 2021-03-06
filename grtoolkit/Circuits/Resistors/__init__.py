from grtoolkit.Math import solveEqs

def Resistance(find, printEq=False, **kwargs):
    """variables: 
                R=resistance
                p=density
                l=length
                A=cross sectional area"""
    eq = list()
    eq.append("Eq(R,p*l/A)")    
    return solveEqs(eq, find, printEq=printEq, **kwargs)
    
def InSeries(r_list):
    """Resistors connected in series is the sum of the individual resistances"""
    return sum(r_list)

def InParallel(r_list):
    sumOfInverse = sum([1/r for r in r_list])
    return 1/sumOfInverse

def voltageDivision(v_in, r_list_ordered, showWork=False):
    """
    Voltage is divided among the resistors in direct proportion to their resistances; 
    the larger the resistance, the larger the voltage drop.
    """
    r_total = sum(r_list_ordered)
    voltages = [r/r_total*v_in for r in r_list_ordered]
    if showWork:
        print("Resistor ordered voltage division: ", voltages)
        print("Adjust directions as necessary after getting result.")
    return voltages

def currentDivision(i_in, r_branch_list_ordered, showWork=False):
    conductances = [Conductance(r) for r in r_branch_list_ordered]
    g_total = sum(conductances)
    currents = [g/g_total*i_in for g in conductances]
    if showWork:
        print("Branch ordered current division: ", currents) 
        print("Adjust directions as necessary after getting result.")
    return currents 

def delta2wye(Ra, Rb, Rc):
    """
    ''------RA-------''''R2'''''''''R3''''
    '''dd''''''''dd'''''''' y'''''y'''''''
    '''''RC''''RB''''''''''''''y''''''''''
    '''''''d''d''''''''''''''''y''''''''''
    ''''''''dd'''''''''''''''''R1'''''''''

    Returns R1, R2, R3
    """
    Rt = Ra+Rb+Rc
    R1 = Rb*Rc/Rt
    R2 = Rc*Ra/Rt
    R3 = Ra*Rb/Rt
    return R1, R2, R3

def wye2delta(R1, R2, R3):
    """
    ''------RA-------''''R2'''''''''R3''''
    '''dd''''''''dd'''''''' y'''''y'''''''
    '''''RC''''RB''''''''''''''y''''''''''
    '''''''d''d''''''''''''''''y''''''''''
    ''''''''dd'''''''''''''''''R1'''''''''

    Returns Ra, Rb, Rc
    """
    Rx = R1*R2 + R2*R3 + R3*R1
    Ra = Rx/R1
    Rb = Rx/R2
    Rc = Rx/R3
    return Ra, Rb, Rc