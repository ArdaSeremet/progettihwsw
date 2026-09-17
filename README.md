# ProgettiHWSW Python Controller 

This Python3 package makes it easier to control ProgettiHWSW relay boards. More detailed explanation will be added later.

This project uses MIT license.

## Publishing

- Create a PyPI API token at https://pypi.org/manage/account/ and add it to your GitHub repo secrets as `PYPI_API_TOKEN`.
- The workflow publishes when you push a semantic version tag (e.g. `v1.2.3`). Create and push a tag with:

```bash
git tag v1.2.3
git push origin v1.2.3
```

The workflow will build `sdist` and `wheel` and publish to PyPI automatically, and create a GitHub Release for the tag.