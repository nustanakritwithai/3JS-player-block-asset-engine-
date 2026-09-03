# V1.8.4 Source Pointer

The deployable Character Prototype Studio V1.8.4 HTML is stored losslessly in:

`deploy/source_v1_8_4/parts/`

`scripts/build_pages.py` concatenates the Base64 parts, decodes XZ, verifies the exact V1.8.4 source checksum, then publishes the reconstructed HTML to `_site/index.html`.

Expected HTML SHA-256:

`d55bd0beca0839bd59fb45a827879293bde6c15de372826bafe6356b2a617484`

The GitHub Pages workflow also regenerates and verifies the native 2048×2048 PBR starter texture pack before deployment.
