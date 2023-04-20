from typing import Type
from typing import Any

from github.Repository import Repository


class BasePolicy:

    def __init__(self, options: Any):
        self.options = options

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__


class PolicyApplicator:
    known_policies: dict[str, type[BasePolicy]] = {}
    policies: list[Any] = []

    def __init__(self):
        pass

    def __repr__(self) -> str:
        return "PolicyApplicator(policies=%r)" % (self.policies)


    def add(self, policy: Any):
        self.policies.append(policy)

    def apply(self, repo: Repository, dry_run: bool = False):
        for policy in self.policies:
            policy.apply(repo, dry_run)

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

