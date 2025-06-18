from visualize_jsonl import parse_jsonl_to_df, plot_basic_diagnostics

profiles = ["resilient", "stress_eater", "fatigue_sensitive"]

for profile in profiles:
    print(f"\n📊 Profile: {profile}")
    df = parse_jsonl_to_df(f"results/synthetic/{profile}.jsonl")
    plot_basic_diagnostics(df, title_prefix=profile)
