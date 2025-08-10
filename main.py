import numpy as np
import pandas as pd

df = pd.read_json("results.json").T
# df.columns = df.columns.astype(int)
df = df.reindex(sorted(df.columns), axis=1)

question_cols = [c for c in df.columns if isinstance(c, int)]

df["correct_answers"] = df[question_cols].sum(axis=1).astype(int)
df["ratio_of_total_questions"] = (df["correct_answers"] / 43) * 100
df["according_to_the_answers_found"] = (df["correct_answers"] / 42) * 100

mean_val = df["correct_answers"].mean()
std_val = df["correct_answers"].std(ddof=1)
df["deviation"] = 0 if std_val == 0 else (df["correct_answers"] - mean_val) / std_val

avg_per_q = df.loc[:, question_cols].mean(axis=0)

def difficulty_fn(x):
    if x < 0.5:
        return 3
    elif x <= 0.75:
        return 2
    else:
        return 1

difficulty_row = pd.Series(np.nan, index=df.columns)
difficulty_row.loc[question_cols] = avg_per_q.apply(difficulty_fn).astype("Int64").values

df.loc["difficulty"] = difficulty_row

difficulty_vals = df.loc["difficulty", question_cols]

df["by_difficulty_level"] = df[question_cols].apply(
    lambda row: ((row == 1) * difficulty_vals).sum(), axis=1
)

df["rash"] = (df["by_difficulty_level"] / 65) * 100

def degree_fn(rash):
    if rash > 70:
        return "A+"
    elif rash >= 65:
        return "A"
    elif rash >= 60:
        return "B+"
    elif rash >= 55:
        return "B"
    elif rash >= 50:
        return "C+"
    elif rash >= 46:
        return "C"
    else:
        return "F"

df["degree"] = df["rash"].apply(lambda x: degree_fn(x) if pd.notnull(x) else np.nan)

df.loc["difficulty", ["by_difficulty_level", "rash", "degree"]] = np.nan

df = df.sort_values(by="correct_answers", ascending=False)

df.to_json("final.json", indent=4)
df.to_excel("final.xlsx")

print(df["correct_answers"].to_dict())


# correct_answers = 35
# overall = (correct_answers / 43) * 100
# findded_answers = (correct_answers / 42) * 100
# deviation = (correct_answers - np.avg(all)) / np.std(all)