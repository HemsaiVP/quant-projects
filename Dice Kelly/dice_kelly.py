import random # Needed for random dice rolls
import statistics #built-in tools for mean, median, etc

#Constants
N_BETS = 200 # Number of bets in a row (UPPERCASE = constant we don't change)
N_SIMS = 10_000 # Number of games to simulate

# Win probability and payout, so we can calculate Kelly in code
P_WIN = 1 / 3
ODDS = 3  # a win pays 3x the stake
KELLY = (ODDS * P_WIN - (1 - P_WIN)) / ODDS  # Kelly formula: (bp - q) / b
fractions = [KELLY / 2, KELLY, 2 * KELLY, 4 * KELLY]  # strategies to compare

def play_one_sequence(fraction):

    """Play N_BETS bets, staking 'fraction' of the bankroll each time.
            Returns the final bankroll, number of wins, bets places, and whether we were ruined"""
    
    #initial conditions
    wins = 0 # counter: starts at 0, BEFORE the loop
    ruined = False # flag : becomes True if we go bust
    count = 0
    bankroll = 100 # starting amount in GBP
    
    for bet in range(N_BETS):

        stake = fraction * bankroll #stake shrinks after losses, grows after wins

        # No borrowing in the model : stop if we cannot afford the next stake
        if bankroll <  1: # fraction betting never hits exactly 0, so treat £1 as minimum bet
            ruined = True
            break
        
        # Roll a fair 6 sided die
        roll = random.randint(1,6)
        count +=1 # Counts number of bets so far

        # Win on a 5 or 6 = 2/6 = P_WIN
        if  roll >=5: 
            # Win pays 3:1, so we gain 3 times the stake
            bankroll += ODDS * stake # changes bankroll
            wins += 1 # counts the win
        else:
            # Any other roll loses the stake
            bankroll -= stake # changes bankroll

    return {"bankroll" : bankroll, "wins": wins, "count" : count, "ruined" : ruined}

random.seed(1)  # fixed seed so results are identical on every run

for fraction in fractions:
    final_bankrolls = [] # empty list to collect each game's result
    for sim in range (N_SIMS):
        result = play_one_sequence(fraction)
        final_bankrolls.append(result["bankroll"]) #add this games result to the end of the list

    assert len(final_bankrolls) == N_SIMS  # every game must produce one result

    #get statistics
    median = statistics.median(final_bankrolls)
    mean = statistics.mean(final_bankrolls)
    ruined_share = sum(b < 1 for b in final_bankrolls) / N_SIMS # share of games that went bust

    print()
    print(f"Fraction {fraction:.3f}: median £{median:,.0f}, mean £{mean:,.0f}, ruined {ruined_share:.1%}")
    print()

