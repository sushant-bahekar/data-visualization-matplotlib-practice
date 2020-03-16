# --------------
import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# Load the dataset and create column `year` which stores the year in which match was played
data_ipl = pd.read_csv(path)
data_ipl['year'] = data_ipl['date'].apply(lambda x : x[:4])

# Plot the wins gained by teams across all seasons
match_wise_data = data_ipl.drop_duplicates(subset='match_code', keep='first').reset_index(drop=True)
total_wins = match_wise_data['winner'].value_counts() 
plot = total_wins.plot(kind='bar', title = "Total no. of wins across seasons 2008-2016", figsize=(7,5))
plt.xticks(fontsize =10 , rotation=90);

# Plot Number of matches played by each team through all seasons
temp_data = pd.melt(match_wise_data, id_vars=['match_code', 'year'], value_vars= ['team1', 'team2'])
matches_played = temp_data.value.value_counts()
plt.figure(figsize=(12,6))
matches_played.plot(x= matches_played.index, y = matches_played, kind = 'bar', title= 'No. of matches played across 9 seasons')
plt.xticks(rotation = 'vertical')
plt.show()

# Performance of top bowlers over seasons
wickets = data_ipl[(data_ipl['wicket_kind']=='bowled')|(data_ipl['wicket_kind']=='caught')|(data_ipl['wicket_kind']=='lbw')|(data_ipl['wicket_kind']=='caught and bowled')]
bowlers_wickets = wickets.groupby(['bowler'])['wicket_kind'].count()

bowlers_wickets.sort_values(ascending = False, inplace = True)

bowlers_wickets[:10].plot(x= bowlers_wickets.index, y = bowlers_wickets, kind = 'barh', colormap = 'Accent');



# How did the different pitches behave? What was the average score for each stadium?
score_per_venue = data_ipl.loc[:, ['match_code', 'venue', 'inning', 'total']]
average_score_per_venue = score_per_venue.groupby(['match_code', 'venue', 'inning']).agg({'total' : 'sum'}).reset_index()
average_score_per_venue = average_score_per_venue.groupby(['venue', 'inning'])['total'].mean().reset_index()
average_score_per_venue = average_score_per_venue[(average_score_per_venue['inning'] == 1) | (average_score_per_venue['inning'] == 2)]
plt.figure(figsize=(19,8))
plt.plot(average_score_per_venue[average_score_per_venue['inning']==1]['venue'],average_score_per_venue[average_score_per_venue['inning']==1]['total'],'-b',marker='o',ms=6,lw=2, label = 'inning1')
plt.plot(average_score_per_venue[average_score_per_venue['inning']==2]['venue'],average_score_per_venue[average_score_per_venue['inning']==2]['total'],'-r',marker='o',ms=6,lw=2, label = 'inning2')
plt.legend(loc = 'upper right', fontsize = 19)
plt.xticks(fontsize = 15, rotation=90)
plt.xlabel('Venues', fontsize=18)
plt.ylabel('Average runs scored on venues', fontsize=16)
plt.show()

# Types of Dismissal and how often they occur
dismissed = data_ipl.groupby(['wicket_kind']).count().reset_index()
dismissed = dismissed[['wicket_kind', 'delivery']]
dismissed = dismissed.rename(columns={'delivery' : 'count'})
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
f.suptitle("Top 5 Dismissal Kind", fontsize=14)

dismissed.plot.bar(ax=ax1, legend=False)
ax1.set_xticklabels(list(dismissed["wicket_kind"]), fontsize=8)

explode =[0.01,0.02,0.1,0.2,0.25,0.4,0.35,0.05,0.05]
properties = ax2.pie(dismissed["count"], labels=None, startangle=150, autopct='%1.1f%%', explode = explode)
ax2.legend(bbox_to_anchor=(1,1), labels=dismissed['wicket_kind'])

# Plot no. of boundaries across IPL seasons
boundaries_data = data_ipl.loc[:,['runs','year']]
boundary_fours = boundaries_data[boundaries_data['runs']==4]
fours = boundary_fours.groupby('year')['runs'].count()
boundary_sixes = boundaries_data[boundaries_data['runs']==6]
sixes = boundary_sixes.groupby('year')['runs'].count()
plt.figure(figsize=(12,8))
plt.plot(fours.index, fours,'-b',marker='o',ms=6,lw=2, label = 'fours')
plt.plot(sixes.index, sixes,'-r',marker='o',ms=6,lw=2, label = 'sixes')
plt.legend(loc = 'upper right', fontsize = 19)
plt.xticks(fontsize = 15, rotation=90)
plt.xlabel('IPL Seasons', fontsize=18)
plt.ylabel('Total 4s and 6s scored across seasons', fontsize=16)
plt.show()

# Average statistics across all seasons
per_match_data = data_ipl.drop_duplicates(subset='match_code', keep='first').reset_index(drop=True)

total_runs_per_season = data_ipl.groupby('year')['total'].sum()
balls_delivered_per_season = data_ipl.groupby('year')['delivery'].count()
no_of_match_played_per_season = per_match_data.groupby('year')['match_code'].count()
avg_balls_per_match = balls_delivered_per_season/no_of_match_played_per_season
avg_runs_per_match = total_runs_per_season/no_of_match_played_per_season
avg_runs_per_ball = total_runs_per_season/balls_delivered_per_season
avg_data = pd.DataFrame([no_of_match_played_per_season, avg_runs_per_match, avg_balls_per_match, avg_runs_per_ball])
avg_data.index =['No.of Matches', 'Average Runs per Match', 'Average balls bowled per match', 'Average runs per ball']
avg_data.T.plot(kind='bar', figsize = (12,10), colormap = 'coolwarm')
plt.xlabel('Season')
plt.ylabel('Average')
plt.legend(loc=9,ncol=4);


