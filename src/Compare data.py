import pandas as pd
import os

compare_file = './output/2026-09-06_badminton_record.csv'
compare_date = os.path.basename(compare_file).split('_')[0]

def find_changes(df1, df2):
    # Merge the two DataFrames on all columns except 'Record Time'
    merged = df1.merge(df2, 
                       on=[col for col in df1.columns 
                           if col not in ['Record Time', 'Available_Courts']], 
                       how='outer', suffixes=('_df1', '_df2'), indicator=True)

    merged['Changes'] = (merged['Available_Courts_df2'].fillna(0) 
                         - merged['Available_Courts_df1'].fillna(0))
    merged = merged[merged['Changes'] != 0]
    merged['Status'] = merged['Changes'].apply(
        lambda x: 'Added' if x > 0 else ('Removed' if x < 0 else 'Unchanged')
    )
    #changes_df = merged[merged['_merge'] == 'right_only'].copy()
    changes_df = merged[[col for col in merged.columns 
                         if not col.endswith('_df1')]
                         ].copy()
    changes_df = changes_df.drop(columns=['_merge'])
    changes_df = changes_df.rename(
        columns={col: col.replace('_df2', '') for col in changes_df.columns}
        )

    return changes_df
    
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
        diff_df_temp = find_changes(df1, df2)
        diff_df = pd.concat([diff_df, diff_df_temp], ignore_index=True)
        df1 = group

diff_df.to_csv(f'./output/{compare_date}_badminton_record_diff_log.csv', 
               index=False)

diff_df_summary = diff_df.groupby(['Record Time', 'Status']).size()
diff_df_summary.to_csv(
    f'./output/{compare_date}_badminton_record_diff_summary.csv'
)