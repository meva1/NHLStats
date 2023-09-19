CREATE DATABASE IF NOT EXISTS nhl_db;
use nhl_db;

CREATE TABLE IF NOT EXISTS player_info (
    player_id int,
    firstName varchar(20),
    lastName varchar(20),
    nationality varchar(20),
    birthCity varchar(30),
    primaryPosition varchar(10),
    birthDate datetime,
    birthStateProvince varchar(50),
    height varchar (10),
    height_cm float,
    weight int,
    shootsCatches varchar (10)
);

CREATE TABLE IF NOT EXISTS team_info (
    team_id int,
    franchiseId int,
    shortName varchar(20),
    teamName varchar(20),
    abbreviation varchar(5),
    link varchar (50)
);

CREATE TABLE IF NOT EXISTS game_skater_stats (
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

CREATE TABLE IF NOT EXISTS game (
    game_id int,
    season varchar(20),
    type varchar(20),
    date_time_GMT varchar(30),
    away_team_id int,
    home_team_id int,
    away_goals int,
    home_goals int,
    outcome varchar(20),
    home_rink_side_start varchar(15),
    venue varchar(50),
    venue_link varchar(50),
    venue_time_zone_id varchar(50),
    venue_time_zone_offset int,
    venue_time_zone_tz varchar(20)
);

CREATE TABLE IF NOT EXISTS game_shifts (
    game_id int,
    player_id int,
    period int,
    shift_start int,
    shift_end int
);

CREATE TABLE IF NOT EXISTS game_plays (
    play_id varchar(20),
    game_id int,
    team_id_for int,
    team_id_against int,
    event varchar(100),
    secondaryType varchar(100),
    x int,
    y int,
    period varchar (10),
    periodType varchar (20),
    periodTime int,
    periodTimeRemaining int,
    dateTime varchar(50),
    goals_away int,
    goals_home int,
    description varchar(255),
    st_x int,
    st_y int
);

CREATE TABLE IF NOT EXISTS game_plays_players (
    play_id varchar(20),
    game_id int,
    player_id int,
    playerType varchar(20)
);

CREATE TABLE IF NOT EXISTS game_goalie_stats (
    game_id int,
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
    decision varchar(10),
    savePercentage float,
    powerPlaySavePercentage float,
    evenStrengthSavePercentage float
);

CREATE TABLE IF NOT EXISTS game_teams_stats (
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
    blocked int,
    startRinkSide varchar(20)
);

CREATE TABLE IF NOT EXISTS game_penalties (
    play_id varchar(20),
    penaltySeverity varchar(20),
    penaltyMinutes int
);

CREATE TABLE IF NOT EXISTS game_goals (
    play_id varchar(20),
    strength varchar(20),
    gameWinningGoal boolean,
    emptyNet boolean
);

CREATE TABLE IF NOT EXISTS game_officials (
    game_id varchar(20),
    official_name varchar(50),
    official_type varchar(20)
);


