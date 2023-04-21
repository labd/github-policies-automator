from github.Organization import Organization
from github.Repository import Repository

from ghpolicy.policy import BasePolicy


class DefaultBranch(BasePolicy):
    def apply(self, org: Organization, repo: Repository, dry_run: bool = False):
        """Make sure the default branch is called main and that the master
        branch is deleted.

        """
        # TODO: Need to make sure we don't create a new issue every run
        # if repo.default_branch not in ('main', 'develop'):
        #     print(f"Creating issue due to incorrect default branch")
        #     if not self.dry_run:
        #         repo.create_issue(
        #             title="Invalid default branch configured",
        #             body="The default branch should be 'main' or 'develop'",
        #         )

        # branches = {b.name: b for b in repo.get_branches()}
        # if 'main' in branches:
        #     branch = branches['main']
        #     if not branch.protected:
        #         if not self.dry_run:
        #             repo.create_issue(
        #                 title="Invalid default branch configured",
        #                 body="The default branch should be 'main' or 'develop'",
        #             )
