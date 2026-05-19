# BATHECOMB

Placeholder for BATHECOMB-specific documentation.

Keep this folder minimal until BATHECOMB-specific scripts or configuration are
needed. Reusable benchmark code should stay in `ml_benchmark/`; MEPRAM-specific
code should stay in `mepram/`.


## Staged mortality modelling

Use the BAcTHECOM wrapper to run staged modelling from an already-preprocessed CSV.

```bash
./.venv/bin/python bacthecom/run_staged_mortality_model.py \
  --database-file playground/preprocess_bacthecom_mortality_filtered.csv \
  --output-dir playground/bacthecom_staged_30d \
  --mortality-horizon-days 30
```

For a 14-day endpoint, set `--mortality-horizon-days 14` (requires a
`mortalidad_14_dias` column in the input CSV).
