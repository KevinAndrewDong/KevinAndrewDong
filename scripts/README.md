# Profile PR checker

A small GitHub REST API integration that checks whether the pull requests linked
from a profile README have been merged. It can also verify the contributor's
GitHub login. It only reads GitHub data and never changes the README.

Requires Python 3 and an authenticated [GitHub CLI](https://cli.github.com/).
Run from the repository root:

```sh
python3 scripts/check_profile_prs.py --author KevinAndrewDong
python3 scripts/check_profile_prs.py /path/to/README.md --author YOUR_LOGIN
```

Exit status: `0` for verified merged PRs, `1` for an unmerged PR, author mismatch,
or missing PR links, and `2` when a file or API response cannot be read.

This checks PR merge status and authorship. It does not verify the surrounding
claims, aggregate search links, or links inside other documents.
