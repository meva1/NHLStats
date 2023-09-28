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
    name varchar(50),
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

CREATE TABLE IF NOT EXISTS game_api (
    game_id int,
    home_id int,
    away_id int,
    game_date date,
    winner varchar(4),
    away_goals int,
    home_goals int
);

CREATE TABLE IF NOT EXISTS game_goalie_stats_api (
    game_id int,
    name varchar(50),
    player_id int,
    team_id int,
    timeOnIce int,
    assists int,
    goals int,
    pim int,
    shots int,
    saves int,
    powerPlaySaves int,
    shortHandedSaves int,
    evenSaves int,
    shortHandedShotsAgainst int,
    evenShotsAgainst int,
    powerPlayShotsAgainst int,
    decision varchar(1),
    savePercentage float
);

CREATE TABLE IF NOT EXISTS game_json (
    id int auto_increment primary key,
    copyright longtext,
    gamePk longtext,
    link longtext,
    metaData longtext,
    gameData longtext,
    liveData longtext
);
