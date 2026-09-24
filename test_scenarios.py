import io
from contextlib import redirect_stdout

from environment import Environment
from agent import RescueAgent

from config import GRID_SIZE


# =========================================================
# TEST SETTINGS
# =========================================================

MAX_STEPS = 300


# =========================================================
# RUN ONE SCENARIO
# =========================================================

def run_scenario(scenario):

    environment = Environment(
        GRID_SIZE,
        scenario
    )

    agent = RescueAgent(
        environment
    )

    for _ in range(MAX_STEPS):

        if agent.mission_complete:
            break

        # Silence the detailed console output.
        with redirect_stdout(io.StringIO()):

            agent.step()

    metrics = agent.get_metrics()

    return metrics


# =========================================================
# RUN ALL SCENARIOS
# =========================================================

print()
print("==============================================")
print("     WUMPUS RESCUE SCENARIO TEST SUITE")
print("==============================================")


for scenario in range(1, 4):

    metrics = run_scenario(
        scenario
    )

    print()
    print("----------------------------------------------")
    print(f"SCENARIO {scenario}")
    print("----------------------------------------------")

    print(
        f"Mission Complete : "
        f"{metrics['mission_complete']}"
    )

    print(
        f"Steps           : "
        f"{metrics['steps']}"
    )

    print(
        f"Visited Cells   : "
        f"{metrics['visited_cells']}"
    )

    print(
        f"Exploration     : "
        f"{metrics['exploration_moves']}"
    )

    print(
        f"Backtracks      : "
        f"{metrics['backtracks']}"
    )

    print(
        f"Return Moves    : "
        f"{metrics['return_moves']}"
    )

    print(
        f"Inference Cycles: "
        f"{metrics['inference_cycles']}"
    )

    print(
        f"Refused Moves   : "
        f"{metrics['refused_moves']}"
    )


print()
print("==============================================")
print("                TEST COMPLETE")
print("==============================================")