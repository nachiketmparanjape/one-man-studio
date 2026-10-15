# Studio standard: secrets and security

**Status:** active · **Adopted:** 2026-10-14

One leaked key ends the studio. This standard exists so secret handling
is written down, not remembered — because "remembered" fails exactly
once, permanently.

## The rules

1. **No secret ever enters git.** Not in code, not in config files, not
   in a comment, not in a screenshot pasted into a doc. If it was
   committed, it's compromised: rotate it immediately, don't just
   delete it (git history remembers).
2. **Server secrets live in Firebase Secret Manager.**
   `firebase functions:secrets:set NAME`, accessed via `defineSecret`
   and passed in the function's `secrets:` option — never
   `process.env` for real secrets, never hardcoded. Each function
   declares only the secrets it needs.
3. **Client config is not a secret.** Firebase web API keys are public
   by design (they're restricted by Firestore rules and App Check, not
   by secrecy). They still live in git-ignored `.env` files locally —
   not because they're secret, but because environments differ.
4. **`.env` is git-ignored; `.env.example` is committed.** The example
   lists every variable with empty values and a comment saying where
   the real value comes from. A new checkout is one copy away from
   working.
5. **Local-only credentials** (PATs, CLI tokens) live at `~/.config/`
   with `600` permissions, never in the repo, never in chat, never in
   a doc. They are never echoed, pasted, or logged.
6. **Fail fast on missing config.** Validate required env/secrets at
   startup and crash immediately with a clear message naming the
   missing variable. A server that starts half-configured fails in
   confusing ways at 2 AM.

## The security checklist (every cut)

- [ ] No secrets, keys, tokens, or credentials in the diff — search it
      before committing, don't eyeball it
- [ ] Callable checks `request.auth` first (not `request.data.uid`);
      input validated before use
- [ ] Firestore/Storage rules: least privilege per path; any rules
      change carries succeed/fail tests (see testing standard)
- [ ] Error messages and logs contain no internals, stack traces, or
      secrets (see error-handling standard)
- [ ] New endpoints: is App Check enforcement appropriate? (public
      endpoints that cost money per call: yes)

## If something leaks

1. Rotate the secret immediately (new value in Secret Manager, old one
   revoked at the provider).
2. Check git history for how long it was exposed.
3. Check logs for whether it was ever printed.
4. Then fix the process hole that let it happen — the leak is a symptom.

Speed matters more than elegance here. Rotate first, investigate second.
