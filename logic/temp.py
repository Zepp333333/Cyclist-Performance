#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved


import pandas as pd
start = [4, 5, 12, 14, 15, 18, 25]
end =   [7, 8, 13, 16, 24, 24, 50]
mean =  [3, 2, 5,  6,  4,  4,  6]

df = pd.DataFrame()
df['start'] = start
df['end'] = end
df['mean'] = mean

intervals = pd.arrays.IntervalArray.from_arrays(df.start, df.end, closed='both')
result = []


def _pick_interval_with_max_mean(overlapping_intervals):
    return overlapping_intervals.loc[overlapping_intervals['mean'] == overlapping_intervals['mean'].max()].iloc[0]


def _make_tuple(selected_interval) -> tuple[int, int]:
    return int(selected_interval['start']), int(selected_interval['end'])


for i in intervals:
    overlap_mask = intervals.overlaps(i)
    if overlap_mask.sum() < 1:  # intervals has no overlaps. Append it's left & right  to the result
        result.append((int(i.left), int(i.right)))
    # Otherwise, we interval has overlaps
    overlapping_intervals = df[overlap_mask]    # get overlapping intervals including their means
    selected_interval = _pick_interval_with_max_mean(overlapping_intervals)
    interval_tuple = _make_tuple(selected_interval)
    if interval_tuple not in result:
        result.append(interval_tuple)


print(result)



# for i in intervals:
#     overlap = intervals.overlaps(i)
#
#     if overlap.sum() > 1:
#         print(overlap)
#
#         overlapping_intervals = df[overlap]
#         print(overlapping_intervals)
#         # selected_interval_position = overlapping_intervals['mean'].argmax()
#         selected_interval = overlapping_intervals.loc[overlapping_intervals['mean'] == overlapping_intervals['mean'].max()]
#         print(f'selected interval:\n {selected_interval}, {type(selected_interval)}')
#         print(f"{int(selected_interval['start'])}")
#         selected_interval_list = [int(selected_interval['start']), int(selected_interval['end'])]
#         print(f'list = {selected_interval_list}, {type(selected_interval_list)}')
#         # selected_interval = overlapping_intervals.iloc[0][1]
#
#         if selected_interval_list not in non_overlapping_intervals:
#             non_overlapping_intervals.append(selected_interval_list)
#     else:
#         non_overlapping_intervals.append([int(i['start']), int(i['end'])])
