# Dead links found during discovery

Checked 2026-08-03. Every candidate URL got a `HEAD` request with redirects
followed; anything that did not answer `200` is listed here instead of being
put in `projects.json`.

Method: `gh api users/maqsudjon-cell/repos --paginate` (179 repos, 166 with
Pages), each repo's `CNAME`, the sitemaps of `maqsudjon.com` and
`flarestamina.com`, and the links in the root site's own `index.html`.

## 404 — repo has Pages enabled, nothing is served

| Repo | URL tried | Code |
|---|---|---|
| `Ecotravelvocabs` | `https://flarestamina.com/Ecotravelvocabs/` | 404 |
| `pangeya-ai-` | `https://pangeya-ai.vercel.app/` | 404 |
| `pangeya-ai-` | `https://flarestamina.com/pangeya-ai-/` | 404 |
| `tracker` | `https://flarestamina.com/tracker/` | 404 |
| `trucking` | `https://flarestamina.com/trucking/` | 404 |

## 404 — directory index missing, but the app itself is alive

| Repo | URL tried | Code |
|---|---|---|
| `pangeya-essay-platform-` | `https://flarestamina.com/pangeya-essay-platform-/` | 404 |

`https://flarestamina.com/pangeya-essay-platform-/index-14.html` answers 200,
and the root site links to that file directly. The directory has no
`index.html`, so the bare folder URL 404s. Worth adding a redirect.

## Connection failure — domain does not resolve or the TLS handshake fails

| Domain | Code | Where it is used |
|---|---|---|
| `minnos.cc` | `000` | **Stack card 02, Minnos** |
| `pierics.com` | `000` | **Stack card 05, Pierics** |

These two are linked from the Stack on this page and from the root site.
`curl` cannot complete a connection to either. Pierics is still reachable at
`https://pierics.vercel.app/` and at `https://flarestamina.com/pierics/`, both
200 — only the custom domain is down. No live URL was found for Minnos.

The Stack was left untouched as instructed, so both links still ship as-is.
