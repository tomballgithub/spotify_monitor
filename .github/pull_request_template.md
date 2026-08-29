# What this changes

<!-- What the change does and why. Link the issue it closes. -->

## Validation

<!-- Which of these you ran and anything that failed. -->

- [ ] `python -m pytest`
- [ ] `mkdocs build --strict`, for a documentation change
- [ ] `docker build .`, for a container or packaging change
- [ ] Exercised against a real Spotify account, for a token, monitoring-loop or metadata-backend change

<!-- A token or monitoring change is not verified by the offline suite alone, which never contacts
     Spotify or Last.fm. Say what you ran it against, without usernames or credentials. -->

## Documentation and release notes

- [ ] User-facing behavior is documented under `docs/`
- [ ] `RELEASE_NOTES.md` carries an entry or the change is not user facing

## Anything a reviewer should know

<!-- Trade-offs, follow-up work or parts you are unsure about. -->

<!-- Never include your sp_dc cookie, Protobuf login files, Spotify refresh tokens, Last.fm API keys,
     SMTP passwords, webhook URLs, ntfy tokens or the friends you monitor in a pull request. -->
