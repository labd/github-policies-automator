import copy
from github.Organization import Organization
from github.Team import Team
from github.Repository import Repository

from ghpolicy.policy import BasePolicy


class TeamPermissionsPolicy(BasePolicy):

    def __init__(self, options: list[dict[str, str]]):
        self.options = options

    def merge(self, other: "TeamPermissionsPolicy") -> "TeamPermissionsPolicy":
        data = copy.deepcopy(self.options)
        data.extend(other.options)
        return TeamPermissionsPolicy(data)

    def apply(self, org: Organization, repo: Repository, dry_run: bool = False):
        """Make sure the teams are correctly asigned to the repository and have
        the correct permissions.

        """
        teams: dict[str, Team] = {t.slug: t for t in repo.get_teams()}

        for name, team in teams.items():
            if name not in self.teams:
                if dry_run:
                    print(f"Would remove {team.name} from {repo.name}")
                else:
                    print(f"Removing {team.name} from {repo.name}")
                    team.remove_from_repos(repo)
            else:
                wanted_permission = self.teams[name]
                permissions = team.get_repo_permission(repo)

                if not permissions.raw_data[wanted_permission]:
                    if dry_run:
                        print(f"Would set {team.name} permission to {wanted_permission}")
                    else:
                        print(f"Setting {team.name} permission to {wanted_permission}")
                        team.set_repo_permission(repo, wanted_permission)

        for name, permission in self.teams.items():
            if name not in teams:
                team = org.get_team_by_slug(name)

                if dry_run:
                    print(f"Would add {team.name} to {repo.name}")
                else:
                    print(f"Adding {team.name} to {repo.name}")
                    team.set_repo_permission(repo, permission)


    @property
    def teams(self) -> dict[str, str]:
        items = self.options or []
        result = {}

        for obj in items:
            name = obj.get('name')
            permission = obj.get('permission')

            if not name or not permission:
                raise Exception("name and permission are required")

            result[name] = permission

        return result
