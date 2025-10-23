# Final Launch Checklist

- [ ] Fix the `pip check` failure (investigate the distribution reporting `version=None` and ensure all installed packages have valid version metadata).
- [ ] Update release metadata to a finalized version (remove the `.dev` suffix from `src/ariadne/_version.py` via `setuptools_scm` tagging and ensure the package builds as the intended release).
- [ ] Reconcile documentation/package naming so every reference points to the PyPI package `ariadne-router` (not `ariadne-quantum-router`).
- [ ] Once the above are complete, rerun `pytest`, `ruff`, `mypy`, and `pip check` to confirm a clean pre-launch state.
- [ ] Perform a final packaging dry run (`python -m build` + `twine check dist/*`) and verify install from the built artifacts.
