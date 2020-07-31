import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


class Team:
    def __init__(self, team_df):
        self.players = team_df['name']
        self.average_per_skill = self._get_average_skills_vector(team_df).reset_index(drop=True)
        self.average_skill = float(np.mean(self.average_per_skill))
        self.players_skills = team_df.drop(['name', 'cluster'], axis=1)

    @staticmethod
    def _get_average_skills_vector(team_df):
        skills_df = team_df.drop(['name', 'cluster'], axis=1)
        return skills_df.mean(axis=0)


class Match:
    def __init__(self, team_a, team_b):
        self.team_a = team_a
        self.team_b = team_b
        self.absolute_skill_differences_vector = self._average_difference(absolute=True)
        self.regular_skill_differences_vector = self._average_difference()
        self.total_absolute_difference_per_skill = float(sum(self.absolute_skill_differences_vector.tolist()))
        self.total_regular_difference_per_skill = abs(float(sum(self.regular_skill_differences_vector.tolist())))
        self.mean_absolute_difference = float(np.mean(self.absolute_skill_differences_vector.tolist()))
        self.mean_regular_difference = abs(float(np.mean(self.regular_skill_differences_vector.tolist())))

    def _average_difference(self, absolute=True):
        return np.abs(self.team_a.average_per_skill - self.team_b.average_per_skill) if absolute else self.team_a.average_per_skill - self.team_b.average_per_skill

    def _sum_of_difference_by_player(self):
        return sum(sum(self.team_a.players_skills.values - self.team_b.players_skills.values))


class MatchCreator:
    def __init__(self, available_players, players_per_team=5, player_types=1):
        self.player_types = player_types
        self.players_table = self._create_players_table(available_players)
        self.players_per_team = players_per_team

    def create_balanced_match(self, iterations=2000, balance_each_skill=False, compensate_differences=False):
        min_match = None
        for i in range(iterations):
            team_1_df = self._sample_players(self.players_table)
            team_2_df = self.players_table[~self.players_table['name'].isin(team_1_df['name'])]
            match = Match(team_a=Team(team_1_df), team_b=Team(team_2_df))
            if min_match is None:
                min_match = match
            else:
                if balance_each_skill and not compensate_differences:
                    new_match_better_than_current_min = match.mean_absolute_difference < min_match.mean_absolute_difference
                elif balance_each_skill and compensate_differences:
                    new_match_better_than_current_min = match.mean_regular_difference < min_match.mean_regular_difference
                elif not balance_each_skill and not compensate_differences:
                    new_match_better_than_current_min = match.total_absolute_difference_per_skill < min_match.total_absolute_difference_per_skill
                else:
                    new_match_better_than_current_min = match.total_regular_difference_per_skill < min_match.total_regular_difference_per_skill
                if new_match_better_than_current_min:
                    min_match = match
        return min_match

    def _sample_players(self, players_table):
        clusters = set(players_table['cluster'])
        merged_df = None
        for cluster in clusters:
            df_cluster = players_table[players_table['cluster'] == cluster]
            if len(df_cluster) > 0:
                sampled_player = df_cluster.sample(n=1)
                if merged_df is None:
                    merged_df = sampled_player
                elif len(merged_df) < self.players_per_team:
                    merged_df = pd.concat([merged_df, sampled_player])
                else:
                    continue
        players_to_complete = self.players_per_team - len(merged_df)
        if players_to_complete > 0:
            not_chosen_yet = players_table[~players_table['name'].isin(merged_df['name'])]
            merged_df = pd.concat([merged_df, not_chosen_yet.sample(n=players_to_complete, replace=False)])
        return merged_df

    def _create_players_table(self, players):
        players_list = []
        for player in players:
            player_dict = {}
            player_dict['name'] = player['name']
            for skill in player['skills']:
                player_dict[skill['name']] = skill['strength']
            players_list.append(player_dict)
        players_table = pd.DataFrame(players_list)
        only_skills = players_table.drop('name', axis=1)
        clustered_players = KMeans(n_clusters=self.player_types).fit(only_skills)
        players_table['cluster'] = clustered_players.labels_
        return players_table


class MatchCreatorReport:
    def __init__(self, match):
        self.match = match
        self.skill_name_list = self.match.team_a.players_skills.columns

    def _skill_list_to_dictionary(self, skill_list):
        final_skill_list = []
        for i, skill in enumerate(skill_list):
            final_skill_list.append({'name': self.skill_name_list[i],
                                     'value': skill})
        return final_skill_list

    def create_report(self, players_repository):
        return {
            'teams': {
                'team_1': {'players': [players_repository.get_player_by_name(player) for player in self.match.team_a.players.tolist()],
                           'skills': self._skill_list_to_dictionary(self.match.team_a.average_per_skill.tolist()),
                           'average_skill': self.match.team_a.average_skill},
                'team_2': {'players': [players_repository.get_player_by_name(player) for player in self.match.team_b.players.tolist()],
                           'skills': self._skill_list_to_dictionary(self.match.team_b.average_per_skill.tolist()),
                           'average_skill': self.match.team_b.average_skill}
            },
            'skill_differences': {
                'average_difference': self.match.mean_absolute_difference,
                'difference_per_skill': self._skill_list_to_dictionary(self.match.absolute_skill_differences_vector.tolist())
            }
        }


