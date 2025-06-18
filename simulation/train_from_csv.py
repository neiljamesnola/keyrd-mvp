from nudge_logic import train_q_table_from_csv, save_q_data

def main():
    input_csv = "output/full_step_log.csv"  # or replace with real-world log
    output_json = "output/q_data.json"

    print(f"Loading from {input_csv} and updating Q-table...")
    train_q_table_from_csv(input_csv)
    save_q_data(output_json)
    print(f"Q-table saved to {output_json}")

if __name__ == "__main__":
    main()
