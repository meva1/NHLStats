-- Calculate the collective win/loss record of all teams playing after more than 5 days of rest

with ng as (select gts.team_id, gts.hoa, g.home_id, g.away_id, g.game_id, g.winner, g.game_date,
lead(g.game_date) over (order by gts.team_id asc, g.game_date asc) nextgame
from game_teams_stats_api gts inner join game_api g on gts.game_id = g.game_id and (gts.team_id = g.home_id or gts.team_id = g.away_id))
select
sum(CASE
        WHEN team_id = home_id and hoa = winner THEN 1
        WHEN team_id = away_id and hoa = winner THEN 1
        ELSE 0 END) as wins,
sum(CASE
        WHEN team_id = home_id and hoa != winner THEN 1
        WHEN team_id = away_id and hoa != winner THEN 1
        ELSE 0 END) as losses
from ng
where date_sub(nextgame, interval 5 day) > game_date
;

-- Calculate the number of games with total goals over/under 6 when two of the specified goaltenders face each other

select
sum(CASE
        WHEN g.away_goals + g.home_goals >= 6 THEN 1
        ELSE 0 END) over_total,
sum(CASE
        WHEN g.away_goals + g.home_goals < 6 THEN 1
        ELSE 0 END) under_total
from game_api g inner join game_goalie_stats_api ggs1
on g.game_id = ggs1.game_id and g.away_id = ggs1.team_id
    and ggs1.name in ('Linus Ullmark','Filip Gustavsson', 'Antti Raanta', 'Jeremy Swayman', 'Ilya Samsonov', 'Ilya Sorokin', 'Connor Hellebuyck', 'Jake Oettinger',
                     'Alexandar Georgiev', 'Jusse Saros', 'Igor Shesterkin', 'Frederik Andersen', 'Logan Thompson', 'Adin Hill')
inner join game_goalie_stats_api ggs2
on g.game_id = ggs2.game_id and g.home_id = ggs2.team_id
    and ggs2.name in ('Linus Ullmark','Filip Gustavsson', 'Antti Raanta', 'Jeremy Swayman', 'Ilya Samsonov', 'Ilya Sorokin', 'Connor Hellebuyck', 'Jake Oettinger',
                     'Alexandar Georgiev', 'Jusse Saros', 'Igor Shesterkin', 'Frederik Andersen', 'Logan Thompson', 'Adin Hill')
order by g.game_id asc;

-- Rank the teams by points

select distinct t.shortName, t.teamName,
sum(CASE
        WHEN gtsa.won = True THEN 2
        WHEN gtsa.won = False and gtsa.settled_in in ('OT', 'SO') THEN 1
        ELSE 0 END) over (partition by gtsa.team_id) points
from game_teams_stats_api gtsa left join team_info t on gtsa.team_id = t.team_id
order by points desc;

-- Players with more than 100 faceoffs taken who have the highest faceoff percentage

with fop as(select distinct name, round(sum(faceoffwins) over (partition by player_id) / sum(faceofftaken) over (partition by player_id),3) face_off_pct, sum(faceofftaken) over (partition by player_id) taken_total
from game_skater_stats_api
order by face_off_pct desc)
select name, face_off_pct from fop
where taken_total > 100
limit 50;

-- Games where multiple players scored 4+ points

select distinct g.game_id, gss1.name, gss1.goals, gss1.assists, gss2.name, gss2.goals, gss2.assists
from game_api g inner join game_skater_stats_api gss1 on g.game_id = gss1.game_id
inner join game_skater_stats_api gss2 on g.game_id = gss2.game_id and gss1.player_id != gss2.player_id
where gss1.goals + gss1.assists >=4 and gss2.goals + gss2.assists >= 4;


