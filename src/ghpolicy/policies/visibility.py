from github.Organization import Organization
from github.Repository import Repository

from ghpolicy.policy import BasePolicy


class VisibilityInternalPolicy(BasePolicy):
    def merge(self, other: "VisibilityInternalPolicy") -> "VisibilityInternalPolicy":
        return VisibilityInternalPolicy(None)

    def apply(self, org: Organization, repo: Repository, dry_run: bool = False):
        """Make sure the repository is correctly set to private or internal.

        Although the GitHub Python SDK doesn't support internal visibility. If
        the visibility is not internal then always set the repository to private.

        """
        # if not cfg.visibility:
        #     return

        # if repo.visibility != cfg.visibility:
        #     print(f"Setting visibility to {cfg.visibility}")
        #     if not self.dry_run:
        #         if cfg.visibility == 'internal':
        #             # GitHub Python SDK Doesn't support this yet
        #             raise Exception("internal visibility is not supported")
        #         else:
        #             repo.edit(private=True)
