import pickle
import pandas as pd

with open("q_table_QLearner.pkl", "rb") as f:
    q_table = pickle.load(f)

print(q_table)

data = []
for state, actions in q_table.items():
    player_pos, opponent_pos, prop_id = state
    for action, value in actions.items():
        data.append({
            'player_pos': player_pos,
            'opponent_pos': opponent_pos,
            'property_id': prop_id,
            'action': action,
            'Q_value': value
        })

df = pd.DataFrame(data)
print(df)
