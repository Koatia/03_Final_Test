# Re-import necessary modules and re-load the dataset to recreate previous steps
import pandas as pd

file_path = 'ab_stats.csv'
ab_stats_df = pd.read_csv(file_path)

# Filter for users with at least one purchase (num_purchases > 0)
paying_users = ab_stats_df[ab_stats_df['num_purchases'] > 0]

# Group by A/B group and calculate the total revenue and number of paying users
grouped_data = paying_users.groupby('ab_group').agg(
    total_revenue=('revenue', 'sum'),
    paying_users=('revenue', 'count')
)

# Calculate ARPPU for each group
grouped_data['ARPPU'] = grouped_data['total_revenue'] / grouped_data['paying_users']

# import ace_tools as tools
# tools.display_dataframe_to_user(name="ARPPU Calculation", dataframe=grouped_data)
print(grouped_data)