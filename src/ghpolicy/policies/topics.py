import copy

from ghpolicy.policy import BasePolicy
from github.Organization import Organization
from github.Repository import Repository


class TopicsContainsPolicy(BasePolicy):
    def __init__(self, options: list[str]):
        self.options = options

    def apply(self, org: Organization, repo: Repository, dry_run: bool = False):
        pass

    def merge(self, other: "TopicsContainsPolicy") -> "TopicsContainsPolicy":
        data = copy.deepcopy(self.options)
        data.extend(other.options)
        return TopicsContainsPolicy(data)
