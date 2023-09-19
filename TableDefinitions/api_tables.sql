use nhl_db;

CREATE TABLE IF NOT EXISTS game_teams_stats_api (
    game_id int,
    team_id int,
    HoA varchar(10),
    won boolean,
    settled_in varchar(20),
    head_coach varchar(30),
    goals int,
    shots int,
    hits int,
    pim int,
    powerPlayOpportunities int,
    powerPlayGoals int,
    faceOffWinPercentage float,
    giveaways int,
    takeaways int,
    blocked int
);

CREATE TABLE IF NOT EXISTS game_skater_stats_api (
    game_id int,
    player_id int,
    team_id int,
    timeOnIce int,
    assists int,
    goals int,
    shots int,
    hits int,
    powerPlayGoals int,
    powerPlayAssists int,
    penaltyMinutes int,
    faceoffWins int,
    faceoffTaken int,
    takeaways int,
    giveaways int,
    shortHandedGoals int,
    shortHandedAssists int,
    blocked int,
    plusMinus int,
    evenTimeOnIce int,
    shortHandedTimeOnIce int,
    powerPlayTimeOnIce int
);

