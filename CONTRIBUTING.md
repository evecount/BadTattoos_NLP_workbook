# Contributing to Project Ink & Cotton

Thank you for contributing to **Project Ink & Cotton: Deconstructing Bad Tattoos & Novelty Graphic Tees with NLP**!

We welcome submissions of new tattoo blunders, ironic graphic tee slogans, and NLP parsing exercises.

---

## Adding Slogans

Add new entries to `data/tattoos_raw.csv` or `data/graphic_tees_raw.csv` following the existing column schemas:
- `tattoos_raw.csv`: `id,category,raw_text,intended_text,body_placement,is_typo`
- `graphic_tees_raw.csv`: `id,category,raw_text,intended_text,theme,has_ambiguity`

Rebuild the combined JSON corpus:
```bash
python -c "
import pandas as pd
from inkcotton.cleaner import SloganCleaner

cleaner = SloganCleaner()
tattoos = cleaner.process_file('data/tattoos_raw.csv')
tees = cleaner.process_file('data/graphic_tees_raw.csv')
pd.concat([tattoos, tees], ignore_index=True).to_json('data/combined_slogans_corpus.json', orient='records', indent=2)
print('Updated corpus!')
"
```

---

## Testing

Ensure all tests pass before opening a Pull Request:

```bash
# Run 8-module student autograder suite
python tests/autograde_checks.py

# Run unit tests
python -m unittest discover tests
```

---

## License

By contributing, you agree that your code will be licensed under the MIT License.
