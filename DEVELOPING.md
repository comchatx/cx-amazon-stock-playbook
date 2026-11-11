# Developing cx-replace-me

REPLACE: how the package works, for a developer.

## Install

```bash
pi install npm:@comchatx/cx-replace-me
```

## Develop

```bash
npm ci
npm run typecheck
npm test
```

## Release

A tag `v<version>` on `main`, the version in `package.json`, runs `.github/workflows/release.yml`, which publishes through npm trusted publishing. WRITING-A-PACKAGE.md, "Shipping it", gives the steps before the first release.
