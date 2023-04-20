from github.Team import Team
from github.Repository import Repository

from ghpolicy.policy import BasePolicy


class TeamPermissionsPolicy(BasePolicy):

    def __init__(self, options: list[dict[str, str]]):
        self.options = options

    def apply(self, repo: Repository, dry_run: bool = False):
        """Make sure the teams are correctly asigned to the repository and have
        the correct permissions.

        """
        teams: dict[str, Team] = {t.name: t for t in repo.get_teams()}

        for name, team in teams.items():
            if name not in self.teams:
                print(f"Removing {team.name} from {repo.name}")
                if not dry_run:
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
