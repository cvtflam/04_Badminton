import pandas as pd
import os

compare_file = './output/2026-09-05_badminton_record.csv'
compare_date = os.path.basename(compare_file).split('_')[0]

def compare_data(df1, df2):
    # Tag each DataFrame with its status
    df1_tagged = df1.assign(Status='Removed')
    df2_tagged = df2.assign(Status='Added')

    # Combine both DataFrames
    combined = pd.concat([df1_tagged, df2_tagged], ignore_index=True)
    
    # Identify feature columns (excluding 'Status')
    feature_cols = list(df1.drop(columns=['Record Time']).columns)
    
    # Drop rows that appear in both DataFrames (keep=False removes both copies)
    comparison_df = combined.drop_duplicates(subset=feature_cols, keep=False)
    
    return comparison_df

df = pd.read_csv(compare_file)
df_by_time = df.groupby('Record Time')
df_by_time_list = list(df_by_time)

df1 = pd.DataFrame()
df2 = pd.DataFrame()
diff_df = pd.DataFrame()
for time, group in df_by_time_list:
    if df1.empty:
        df1 = group
    else:
        df2 = group
        diff_df_temp = compare_data(df1, df2)
        diff_df = pd.concat([diff_df, diff_df_temp], ignore_index=True)
        df1 = group

diff_df.to_csv(f'./output/{compare_date}_badminton_record_diff.csv', 
               index=False)