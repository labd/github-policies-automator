from github.Team import Team
from github.Repository import Repository

from ghpolicy.policy import BasePolicy


class TopicsContainsPolicy(BasePolicy):

    def apply(self, repo: Repository, dry_run: bool = False):
        pass
