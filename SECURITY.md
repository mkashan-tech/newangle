# Security Policy

## Project Status

NewAngle is an early-stage, public, open-source research project (currently in Phase 0 — repository foundation). There is no deployed production instance, hosted service, or live API at this time. This policy will be expanded as the project gains deployed infrastructure and user data.

## Supported Versions

There are no tagged releases yet. Security reports should be filed against the current `main` branch.

## Reporting a Vulnerability

If you discover a security vulnerability (for example: a committed secret, a credential-handling issue, or — once implemented — an injection, authentication, or data-exposure issue), please report it privately rather than opening a public issue.

- Preferred: open a [GitHub private security advisory](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability) on this repository.
- If that's not available to you, open an issue titled generically (e.g., "Security contact needed") without vulnerability details, and the maintainer will follow up with a private channel.

Please include:
- A description of the issue and its potential impact
- Steps to reproduce, if applicable
- Any relevant logs, commit hashes, or file paths

## Handling of Secrets and Credentials

- No API keys, passwords, personal credentials, or restricted datasets should ever be committed to this repository.
- All secrets are managed via environment variables; see `.env.example` for the (non-sensitive) configuration template.
- If a secret is accidentally committed, it should be treated as compromised: revoke/rotate it immediately, and remove it from history in a dedicated follow-up (git history rewriting is a separate, deliberate action, not a routine one).

## Response

As a solo-maintained project, response times are best-effort. Valid reports will be acknowledged and addressed as soon as practical, with credit given to the reporter unless anonymity is requested.
