# World assets

The snap ships no PROTO files. R2025a downloads them from GitHub and caches
them under `~/.cache/Cyberbotics/Webots/assets`, keyed by `sha1(url)`.
`tesla_city.wbt` pins every `EXTERNPROTO` to the `R2025a` tag.

Webots' downloader opens many parallel streams and sometimes drops some,
leaving the world half-loaded. Fill the gaps one URL at a time:
```bash
grep -o "Cannot download '[^']*'" sim.log | cut -d"'" -f2 | ~/ros2_ws/scripts/warm_webots_assets.sh
```
`webots://` URLs don't work with the snap (they resolve to `$WEBOTS_HOME`,
which has no PROTOs). They work on a source build like the Orin's.

On a campus network behind a captive portal, downloads fail silently once the
portal session expires; log in again and retry.
