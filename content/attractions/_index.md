---
title: "Attractions"
# Booths are data, not pages: no public /attractions/<slug>/ URLs, but the
# cascade keeps them in this section's .Pages so the homepage grid can read
# them (same pattern content/people/ uses).
build:
  render: never
  list: never
cascade:
  build:
    render: never
    list: local
---
