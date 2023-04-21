import functools
import os
import re

import github
from github.Organization import Organization
from github.Repository import Repository

from ghpolicy.policies.team_permission import TeamPermissionsPolicy
from ghpolicy.policies.topics import TopicsContainsPolicy
from ghpolicy.policies.visibility import VisibilityInternalPolicy
from ghpolicy.policy import PolicyApplicator

PolicyApplicator.register("visibility-internal", VisibilityInternalPolicy)
PolicyApplicator.register("topics-contains", TopicsContainsPolicy)
PolicyApplicator.register("team-permissions", TeamPermissionsPolicy)


class Rule:
    def __init__(self, name: str, applicator: PolicyApplicator):
        self.name = name
        self.applicator = applicator
        self._regex = re.compile(name)

    def match(self, name: str) -> bool:
        return bool(self._regex.match(name))

    def merge(self, other: "Rule") -> "Rule":
        return Rule("merged", self.applicator.merge(other.applicator))

    def apply(self, org: Organization, repo: Repository, dry_run: bool = False):
        self.applicator.apply(org, repo, dry_run)

    @classmethod
    def from_config(cls, rule: dict):
        policy = PolicyApplicator.from_config(rule["policies"])
        return cls(rule["name"], policy)

    def __repr__(self):
        return "Rule(name=%r, applicator=%r)" % (self.name, self.applicator)


def run(data: dict, dry_run: bool = False):
    print("Running on %s with dry_run=%r" % (data["organization"], dry_run))

    rules = []
    for rule in data.get("rules", []):
        rule = Rule.from_config(rule)
        rules.append(rule)

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise Exception("GITHUB_TOKEN environment variable not set")

    gh = github.Github(token)
    org = gh.get_organization(data["organization"])
    for repo in org.get_repos():
        matching = [rule for rule in rules if rule.match(repo.name)]
        if not matching:
            continue

        if len(matching) > 1:
            print("Multiple rules matched", repo.name, matching)
            rule = functools.reduce(Rule.merge, matching)
            rule.apply(org, repo, dry_run=dry_run)
        else:
            print("Matched", repo.name, matching[0])
            matching[0].apply(org, repo, dry_run=dry_run)
