from qiskit import Aer, IBMQ, QuantumRegister, ClassicalRegister, QuantumCircuit, execute
import getpass, random, numpy, math

def title_screen ():

    print("\n\n\n\n\n\n\n\n")
    print("            ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗            ")
    print("           ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║            ")
    print("           ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║            ")
    print("           ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║            ")
    print("           ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║            ")
    print("            ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝            ")
    print("")
    print("   ██████╗  █████╗ ████████╗████████╗██╗     ███████╗███████╗██╗  ██╗██╗██████╗ ███████╗")
    print("   ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝██╔════╝██║  ██║██║██╔══██╗██╔════╝")
    print("   ██████╔╝███████║   ██║      ██║   ██║     █████╗  ███████╗███████║██║██████╔╝███████╗")
    print("   ██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ ╚════██║")
    print("   ██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗███████║██║  ██║██║██║     ███████║")
    print("   ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝")
    print("")
    print("                 ___         ___                    _       _         ")
    print(r'                | _ ) _  _  |   \  ___  __  ___  __| | ___ | |__ _  _ ')
    print(r'                | _ \| || | | |) |/ -_)/ _|/ _ \/ _` |/ _ \| / /| || |')
    print(r'                |___/ \_, | |___/ \___|\__|\___/\__,_|\___/|_\_\ \_,_|')
    print("                      |__/                                            ")
    print("")
    print("                       A game played on a real quantum computer!")
    print("")
    print("")
    input("> Press Enter to play...\n").upper()


def play_game():
    # the game variable will be set to False once the game is over
    game = True

    # the variable bombs[X][Y] will hold the number of times position Y has been bombed by player X+1
    bomb = [[0]*5 for _ in range(2)] # all values are initialized to zero

    # set the number of samples used for statistics
    shots = 1024

    # the variable grid[player] will hold the results for the grid of each player
    grid = [{}, {}]

    # ask what kind of quantum device will be used (real or simulated)
    device = ask_for_device()

    # ask players where thir ships are
    shipPos = ask_for_ships()

    while (game):

        # ask both players where they want to bomb, and update the list of bombings so far
        bomb = ask_for_bombs(bomb)

        # now we create and run the quantum programs that implement this on the grid for each player
        qc = []
        for player in range(2):

            # now to set up the quantum program to simulate the grid for this player

            # set up registers and program
            q = QuantumRegister(5)
            c = ClassicalRegister(5)
            qc.append(QuantumCircuit(q, c))

            # add the bombs (of the opposing player)
            for position in range(5):
                # add as many bombs as have been placed at this position
                for _ in range(bomb[(player+1)%2][position]):
                    # the effectiveness of the bomb
                    # (which means the quantum operation we apply)
                    # depends on which ship it is
                    for ship in [0,1,2]:
                        if (position == shipPos[player][ship]):
                            frac = 1/(ship+1)
                            # add this fraction of a NOT to the QASM
                            qc[player].u3(frac * math.pi, 0.0, 0.0, q[position])

            # Finally, measure them
            for position in range(5):
                qc[player].measure(q[position], c[position])

        # compile and run the quantum program
        job = execute(qc, backend=device, shots=shots)
        if not device.configuration().to_dict()['simulator']:
            print("\nWe've now submitted the job to the quantum computer to see what happens to the ships of each player\n(it might take a while).\n")
        else:
            print("\nWe've now submitted the job to the simulator to see what happens to the ships of each player.\n")
        # and extract data
        for player in range(2):
            grid[player] = job.result().get_counts(qc[player])
        print(grid)

        game = display_grid(grid, shipPos, shots)

def ask_for_device ():
    
    d = input("Do you want to play on the real device? (y/n)\n").upper()
    if (d=="Y"):
        device = IBMQ.get_backend('ibmq_5_tenerife') # if real, we use ibmqx4
    else:
        device = Aer.get_backend('qasm_simulator') # otherwise, we use a simulator
        
    return device


def ask_for_ships ():
    
    # we'll start with a 'press enter to continue' type command. But it hides a secret! If you input 'R', the positions will be chosen randomly
    randPlace = input("> Press Enter to start placing ships...\n").upper()

    # The variable ship[X][Y] will hold the position of the Yth ship of player X+1
    shipPos = [ [-1]*3 for _ in range(2)] # all values are initialized to the impossible position -1|

    # loop over both players and all three ships for each
    for player in [0,1]:

        # if we chose to bypass player choice and do random, we do that
        if  randPlace=="R":
            randPos = random.sample(range(5), 3)
            for ship in [0,1,2]:
                shipPos[player][ship] = randPos[ship]
            #print(randPos) #uncomment if you want a sneaky peek at where the ships are
        else:
            for ship in [0,1,2]:

                # ask for a position for each ship, and keep asking until a valid answer is given
                choosing = True
                while (choosing):

                    # get player input
                    position = getpass.getpass("Player " + str(player+1) + ", choose a position for ship " + str(ship+1) + " (0, 1, 2, 3 or 4)\n" )

                    # see if the input is valid and ask for another if not
                    if position.isdigit(): # valid answers have to be integers
                        position = int(position)
                        if (position in [0,1,2,3,4]) and (not position in shipPos[player]): # they need to be between 0 and 5, and not used for another ship of the same player
                            shipPos[player][ship] = position
                            choosing = False
                            print ("\n")
                        elif position in shipPos[player]:
                            print("\nYou already have a ship there. Try again.\n")
                        else:
                            print("\nThat's not a valid position. Try again.\n")
                    else:
                        print("\nThat's not a valid position. Try again.\n")
                        
    return shipPos
                        

def ask_for_bombs ( bomb ):
    
    input("> Press Enter to place some bombs...\n")
    
    # ask both players where they want to bomb
    for player in range(2):
    
        print("\n\nIt's now Player " + str(player+1) + "'s turn.\n")

        # keep asking until a valid answer is given
        choosing = True
        while (choosing):

            # get player input
            position = input("Choose a position to bomb (0, 1, 2, 3 or 4)\n")

            # see if this is a valid input. ask for another if not
            if position.isdigit(): # valid answers  have to be integers
                position = int(position)
                if position in range(5): # they need to be between 0 and 5, and not used for another ship of the same player
                    bomb[player][position] = bomb[player][position] + 1
                    choosing = False
                    print ("\n")
                else:
                    print("\nThat's not a valid position. Try again.\n")
            else:
                print("\nThat's not a valid position. Try again.\n")
                
    return bomb


def display_grid ( grid, shipPos, shots ):
    
    # since this function has been called, the game must still be on
    game = True

    # look at the damage on all qubits (we'll even do ones with no ships)
    damage = [ [0]*5 for _ in range(2)] # this will hold the prob of a 1 for each qubit for each player
        
    # for this we loop over all strings of 5 bits for each player
    for player in range(2):
        for bitString in grid[player].keys():
            # and then over all positions
            for position in range(5):
                # if the string has a 1 at that position, we add a contribution to the damage
                # remember that the bit for position 0 is the rightmost one, and so at bitString[4]
                if (bitString[4-position]=="1"):
                    damage[player][position] += grid[player][bitString]/shots          
        
    # give results to players
    for player in [0,1]:

        input("\nPress Enter to see the results for Player " + str(player+1) + "'s ships...\n")

        # report damage for qubits that are ships, and which have significant damage
        # ideally this would be non-zero damage, but noise means it can happen for ships that haven't been hit
        # so we choose 5% as the threshold
        display = [" ?  "]*5
        # loop over all qubits that are ships
        for position in shipPos[player]:
            # if the damage is high enough, display the damage
            if ( damage[player][position] > 0.1 ):
                if (damage[player][position]>0.9):
                    display[position] = "100%"
                else:
                    display[position] = str(int( 100*damage[player][position] )) + "% "
            #print(position,damage[player][position])
                    
        print("Here is the percentage damage for ships that have been bombed.\n")
        print(display[ 4 ] + "    " + display[ 0 ])
        print(r' |\     /|')
        print(r' | \   / |')
        print(r' |  \ /  |')
        print(" |  " + display[ 2 ] + " |")
        print(r' |  / \  |')
        print(r' | /   \ |')
        print(r' |/     \|')
        print(display[ 3 ] + "    " + display[ 1 ])
        print("\n")
        print("Ships with 95% damage or more have been destroyed\n")

        print("\n")

        # if a player has all their ships destroyed, the game is over
        # ideally this would mean 100% damage, but we go for 95% because of noise again
        if (damage[player][ shipPos[player][0] ]>.9) and (damage[player][ shipPos[player][1] ]>.9) and (damage[player][ shipPos[player][2] ]>.9):
            print ("***All Player " + str(player+1) + "'s ships have been destroyed!***\n\n")
            game = False

        if (game is False):
            print("")
            print("=====================================GAME OVER=====================================")
            print("")


    return game










