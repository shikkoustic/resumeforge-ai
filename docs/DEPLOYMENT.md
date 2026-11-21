# Deploying ResumeForge AI to Streamlit Community Cloud

This has to be done by the owner of the GitHub account, because Streamlit signs in through
GitHub. It takes about two minutes.

## Steps

1. Go to https://share.streamlit.io and sign in with GitHub (`shikkoustic`).
2. Click **Create app** → **Deploy a public app from GitHub**.
3. Fill in:
   - Repository: `shikkoustic/resumeforge-ai`
   - Branch: `main`
   - Main file path: `code/app.py`
   - App URL: choose something stable, for example `resumeforge-ai`
4. Before clicking Deploy, open **Advanced settings → Secrets** and paste:

   ```toml
   GEMINI_API_KEYS = "key1,key2,key3,key4"
   ```

   One key per team member, comma separated, no spaces. Each Google account has its own
   daily quota, so four keys give the live demo roughly four times the headroom. A single
   key allows only about 10 reviews per day, because each review costs two requests.
5. Click **Deploy** and wait for the build.

## After deploying

- Open the URL in a **private/incognito window**. The guidelines are explicit: if an
  evaluator cannot open a link, that part scores 0. Signed out is how they will see it.
- Run one review end to end in that window to confirm the secrets are wired.
- Put the URL in three places: `README.md`, the Milestone 2 PDF cover page, and Q11.

## Notes

- `requirements.txt` lives at the repo root because that is where Streamlit Cloud looks.
- Never commit the keys. They belong only in the Secrets box above, which is not part of
  the repository.
- If the app sleeps from inactivity, the first visitor wakes it; that takes a few seconds.
  Open it yourself shortly before the evaluation window so it is warm.

## Known issue to fix before submitting

Streamlit Community Cloud runs the app from the **repository root**, so it reads
`.streamlit/config.toml` at the root — not `code/.streamlit/config.toml`, which is where
the file currently lives for local development.

Effect: the deployed app ignores the theme and falls back to Streamlit's default (dark
background, red accent), while running `streamlit run app.py` from inside `code/` looks
correct.

Fix, once the UI work is finished:

```bash
mkdir -p .streamlit && git mv code/.streamlit/config.toml .streamlit/config.toml
```

Then run locally from the repository root instead:

```bash
./.venv/bin/streamlit run code/app.py
```

Verify the deployed app in a private window afterwards: the background should be light.
