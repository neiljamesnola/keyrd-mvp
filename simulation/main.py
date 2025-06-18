# main.py

from simulate import simulate_user
from visualize import plot_results

if __name__ == "__main__":
    print("Starting KeyRD simulation...\n")

    history = simulate_user(
        initial_state="tired",
        steps=100,
        user_id="sim_user_1",
        strategy="epsilon_greedy"
    )

    print(f"\nSimulation complete. {len(history)} steps recorded.")
    plot_results(history)
