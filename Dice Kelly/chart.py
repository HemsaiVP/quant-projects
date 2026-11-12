"""Plot final bankroll against bet fraction for the dice Kelly game"""

import random
import statistics
from pathlib import Path

# Third-party package, comes after standard-library imports (PEP 8 ordering)
import matplotlib.pyplot as plt

# Reuse the simulation rather than copying it: one source of truth,
# so a fix in dice_kelly.py automatically applies to the chart too
from dice_kelly import play_one_sequence, STARTING_BANKROLL, SEED, KELLY, N_BETS


# Constants
CHART_SIMS = 2_000 # How many games two simulate each fraction

# Fine steps (0.25%) up to 50%, then 5% steps as it is mostly flat after
FRACTION_GRID = (
        [i / 400 for i in range (1,201)]
         + [i/100 for i in range(55, 96, 5)] # Stops at 95% as betting 100% ends at £0 and log(0) is undefined
    )                                        # Creates array for grid of fractions

def summarise_fraction(fraction, n_sims):
    """Simulate n_sims games at one fraction, returns median, mean and final bankroll
    
        Each game is seeded by its own number, so game k gets identical dice at every fraction (common 
        random numbers), regardless of if the previous game was ruined or not.
        """
    final_bankrolls = []
    for game in range(n_sims):
        # Give a distinct seed per game, still tied to SEED so the whole chart is reproducible
        random.seed(SEED * n_sims + game)
        final_bankrolls.append(play_one_sequence(fraction)["bankroll"])
    return statistics.median(final_bankrolls), statistics.mean(final_bankrolls)

def main():
    """Sweep the fraction grid and collect the median and mean for each point"""
    medians = [] # one value per fraction, ready for plotting
    means = []

    for fraction in FRACTION_GRID:
        median, mean = summarise_fraction(fraction, CHART_SIMS) #unpack the median, mean tuple
        medians.append(median)
        means.append(mean)
        print(f"{fraction:.1%} : median £{median:,.0f}, mean £{mean:,.0f}")

    
    #Both curves on one chart, so the gap between "typical" and "average" outcomes is visible
    plt.plot(FRACTION_GRID, medians, label="Median final bankroll")
    plt.plot(FRACTION_GRID, means, label="Mean final bankroll")

    # Values range from pennies to millions so a log scale is more readable
    plt.yscale("log")

    # Reference lines : the theoretical optimum and break even
    plt.axvline(KELLY, linestyle = "--", color = "grey", label=f"Kelly ({KELLY:.1%})")
    plt.axhline(STARTING_BANKROLL, linestyle = ":", color = "black", label = f"Starting bankroll (£{STARTING_BANKROLL:,.0f})")

    #Labels use constants, not typed numbers so they stay correct if N_BETS changes
    plt.xlabel("Fraction of bankroll bet each round")
    plt.ylabel(f"Final bankroll after {N_BETS} bets (£, log scale)")
    plt.title("Dice Kelly game: final bankroll against bet fraction")
    plt.legend() #key showing which line is which, built from label values

    # Save next to this script, wherever the terminal is, so README link always works
    chart_path = Path(__file__).parent / "kelly_chart.png"
    plt.savefig(chart_path, dpi = 150, bbox_inches = "tight") # dpi = sharpness, tight = trim white margins
    plt.show() # must come after savefig : closing the window clears the figure

    
if __name__ == "__main__":
    main()