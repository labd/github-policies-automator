import copy
from github.Organization import Organization
from github.Repository import Repository

from ghpolicy.policy import BasePolicy


class RepositorySettingsPolicy(BasePolicy):
    def __init__(self, options: dict[str, str]):
        self.options = options

    def merge(self, other: "RepositorySettingsPolicy") -> "RepositorySettingsPolicy":
        data = copy.deepcopy(self.options)
        data.update(other.options)
        return RepositorySettingsPolicy(data)

    def apply(self, org: Organization, repo: Repository, dry_run: bool = False):
        """Apply some repository settings"""
        if repo.archived:
            print(f"[repository-settings] skipping archived repository {repo.name}")
            return
        delete_branch_on_merge = self.options.get("delete-branch-on-merge")
        if delete_branch_on_merge is not None:
            self.apply_delete_branch_on_merge(repo, delete_branch_on_merge, dry_run)

    def apply_delete_branch_on_merge(
        self, repo: Repository, value: bool, dry_run: bool = False
    ):
        if repo.delete_branch_on_merge != value:
            if dry_run:
                print(
                    f"[repository-settings] would set delete_branch_on_merge to {value}"
                )
            else:
                print(
                    f"[repository-settings] setting delete_branch_on_merge to {value}"
                )
                repo.edit(delete_branch_on_merge=value)
