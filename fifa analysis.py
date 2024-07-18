import pandas as pd
import matplotlib.pyplot as plt

# Load the data from CSV files
matches_data = pd.read_csv(r"C:\Users\Harsh_ehn0ysj\Downloads\WorldCupMatches.csv")
players_data = pd.read_csv(r"C:\Users\Harsh_ehn0ysj\Downloads\WorldCupPlayers.csv")
world_cups_data = pd.read_csv(r"C:\Users\Harsh_ehn0ysj\Downloads\WorldCups.csv")

# Display the first few rows of each dataset
print(matches_data.head())
print(players_data.head())
print(world_cups_data.head())

# Clean and preprocess the data
matches_data.drop_duplicates(inplace=True)
players_data.drop_duplicates(inplace=True)
world_cups_data.drop_duplicates(inplace=True)

# Fill NaN values with 0 in goal columns before converting to integers
matches_data['Home Team Goals'] = matches_data['Home Team Goals'].fillna(0).astype(int)
matches_data['Away Team Goals'] = matches_data['Away Team Goals'].fillna(0).astype(int)

# Calculate total goals scored by each team in each World Cup
home_goals = matches_data.groupby(['Home Team Name', 'Year'])['Home Team Goals'].sum().reset_index()
away_goals = matches_data.groupby(['Away Team Name', 'Year'])['Away Team Goals'].sum().reset_index()

# Merge home and away goals to calculate total goals scored
total_goals = pd.merge(home_goals, away_goals, how='outer', left_on=['Home Team Name', 'Year'], right_on=['Away Team Name', 'Year'])
total_goals['Goals Scored'] = total_goals['Home Team Goals'].fillna(0) + total_goals['Away Team Goals'].fillna(0)
total_goals = total_goals[['Home Team Name', 'Year', 'Goals Scored']].rename(columns={'Home Team Name': 'Team'})

# Calculate total goals conceded by each team in each World Cup
home_goals_conceded = matches_data.groupby(['Home Team Name', 'Year'])['Away Team Goals'].sum().reset_index()
away_goals_conceded = matches_data.groupby(['Away Team Name', 'Year'])['Home Team Goals'].sum().reset_index()

# Merge home and away goals conceded to calculate total goals conceded
total_goals_conceded = pd.merge(home_goals_conceded, away_goals_conceded, how='outer', left_on=['Home Team Name', 'Year'], right_on=['Away Team Name', 'Year'])

# Identify the correct columns for goals conceded
total_goals_conceded['Goals Conceded'] = total_goals_conceded['Away Team Goals'].fillna(0) + total_goals_conceded['Home Team Goals'].fillna(0)
total_goals_conceded = total_goals_conceded[['Home Team Name', 'Year', 'Goals Conceded']].rename(columns={'Home Team Name': 'Team'})

# Merge the calculated metrics with the world cups data
world_cup_analysis = world_cups_data.merge(total_goals, left_on=['Winner', 'Year'], right_on=['Team', 'Year'], how='left')
world_cup_analysis = world_cup_analysis.merge(total_goals_conceded, left_on=['Winner', 'Year'], right_on=['Team', 'Year'], how='left')

# Drop unnecessary columns
world_cup_analysis.drop(columns=['Team_x', 'Team_y'], inplace=True)

# Plot goals scored by World Cup winners (Bar Chart)
plt.figure(figsize=(10, 6))
plt.bar(world_cup_analysis['Year'], world_cup_analysis['Goals Scored'])
plt.xlabel('Year')
plt.ylabel('Goals Scored')
plt.title('Goals Scored by World Cup Winners')
plt.xticks(rotation=45)
plt.show()

# Plot goals conceded by World Cup winners (Bar Chart)
plt.figure(figsize=(10, 6))
plt.bar(world_cup_analysis['Year'], world_cup_analysis['Goals Conceded'])
plt.xlabel('Year')
plt.ylabel('Goals Conceded')
plt.title('Goals Conceded by World Cup Winners')
plt.xticks(rotation=45)
plt.show()

# Plot number of matches played by winners each year (Line Chart)
plt.figure(figsize=(10, 6))
plt.plot(world_cup_analysis['Year'], world_cup_analysis['MatchesPlayed'], marker='o', linestyle='-', color='b')
plt.xlabel('Year')
plt.ylabel('Matches Played')
plt.title('Number of Matches Played by World Cup Winners')
plt.xticks(rotation=45)
plt.show()

# Plot attendance over the years (Line Chart)
plt.figure(figsize=(10, 6))
plt.plot(world_cup_analysis['Year'], world_cup_analysis['Attendance'], marker='o', linestyle='-', color='g')
plt.xlabel('Year')
plt.ylabel('Attendance')
plt.title('Attendance Over the Years')
plt.xticks(rotation=45)
plt.show()

# Plot top scoring teams (Horizontal Bar Chart)
top_scoring_teams = total_goals.groupby('Team')['Goals Scored'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.barh(top_scoring_teams.index, top_scoring_teams.values, color='purple')
plt.xlabel('Total Goals Scored')
plt.ylabel('Team')
plt.title('Top Scoring Teams')
plt.gca().invert_yaxis()
plt.show()

# Plot goals scored vs. goals conceded by winners (Scatter Plot)
plt.figure(figsize=(10, 6))
plt.scatter(world_cup_analysis['Goals Scored'], world_cup_analysis['Goals Conceded'], color='red')
plt.xlabel('Goals Scored')
plt.ylabel('Goals Conceded')
plt.title('Goals Scored vs. Goals Conceded by World Cup Winners')
plt.show()

# Plot distribution of matches by stages (Pie Chart)
stage_counts = matches_data['Stage'].value_counts()
plt.figure(figsize=(10, 6))
plt.pie(stage_counts, labels=stage_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Matches by Stages')
plt.show()

