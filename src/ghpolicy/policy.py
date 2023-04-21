from typing import Any, Type

from github.Organization import Organization
from github.Repository import Repository


class BasePolicy:
    def __init__(self, options: Any):
        self.options = options

    def merge(self, other: "BasePolicy") -> "BasePolicy":
        return self.__class__(None)

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__


class PolicyApplicator:
    """Applicator owns the policies and applies them to the repository."""

    known_policies: dict[str, type[BasePolicy]] = {}
    policies: list[Any]

    def __init__(self):
        self.policies = []

    def __repr__(self) -> str:
        return "PolicyApplicator(policies=%r)" % (self.policies)

    def add(self, policy: Any):
        self.policies.append(policy)

    def apply(self, org: Organization, repo: Repository, dry_run: bool = False):
        for policy in self.policies:
            policy.apply(org, repo, dry_run)

    def merge(self, other: "PolicyApplicator") -> "PolicyApplicator":
        """Merge the policies from the other applicator with this one.

        Returns a new PolicyApplicator
        """
        applicator = PolicyApplicator()

        t = {p.__class__.__name__: p for p in self.policies}
        o = {p.__class__.__name__: p for p in other.policies}

        for name, policy in t.items():
            if name in o:
                applicator.add(policy.merge(o[name]))
            else:
                applicator.add(policy)

        for name, policy in o.items():
            if name not in t:
                applicator.add(policy)

        return applicator

    @classmethod
    def register(cls, name: str, policy: Type[BasePolicy]):
        cls.known_policies[name] = policy

    @classmethod
    def from_config(cls, policies: dict) -> "PolicyApplicator":
        applicator = cls()

        for name, options in policies.items():
            if name not in cls.known_policies:
                raise Exception(f"Unknown policy {name}")

            policy = cls.known_policies[name](options)
            applicator.add(policy)

        return applicator
