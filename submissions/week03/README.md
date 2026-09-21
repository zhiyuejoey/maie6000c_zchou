# Week 3 Submission — Individual Readiness Lab

## Student information

- Name: Chou Zhiyue
- Student ID: 21315977
- Repository: https://github.com/zhiyuejoey/maie6000c_zchou
- Checkpoint tag: `w03-readiness`
- Commit SHA: resolve with `git rev-parse 'w03-readiness^{commit}'`.
  The exact resulting SHA is also included in the Canvas submission.

## 1. What I changed

I added one integration regression test for `GET /jobs/{job_id}` when the
requested job does not exist. It requires HTTP 404 and the JSON body
`{"detail": "Job not found"}`.

Before this change, the API already implemented this response, but the normally
collected tests only checked retrieving an existing job. After the change, an
incorrect missing-job status code or error message causes a test failure.
The production endpoint's behavior is unchanged; the bounded change is new
automated coverage of its error contract.

The existing `client` fixture creates a fresh, empty SQLite database for every
test. Consequently, job ID 1 is guaranteed to be missing in this test even if
the running Docker/PostgreSQL system contains a job with that ID. The test uses
the real FastAPI route and database lookup through TestClient, rather than
mocking the endpoint response.

## 2. Files touched

- `tests/integration/test_job_not_found.py`: the new regression test.
- `submissions/week03/README.md`: this explanation and verification record.
- `Dockerfile`: a separate preceding classroom setup commit installs `.[dev]`
  and copies `tests` into the image, enabling the documented Docker test commands.

The test was developed on `test/missing-job-404`, separately from the Dockerfile
setup commit. No production API code or database schema was changed.

## 3. How to run and verify

Prerequisites: Git, Docker Desktop with its engine running, and access to this
private repository. Commands below are for a macOS terminal.

```bash
git clone https://github.com/zhiyuejoey/maie6000c_zchou.git
cd maie6000c_zchou
git checkout w03-readiness
cp -n .env.example .env
docker compose config --quiet
docker compose up --build -d
docker compose ps
```

The default API host port is 8000; AI is 8100 and PostgreSQL is 5432. If ports
are occupied, adjust the host ports in `.env`. For an existing checkout after
editing tests, run `docker compose build api` to include the saved test files.

Run the focused test, regression suite, and lint checks:

```bash
docker compose run --rm --no-deps api pytest -q tests/integration/test_job_not_found.py
docker compose run --rm --no-deps api pytest -q tests/unit tests/integration
docker compose run --rm --no-deps api ruff check .
```

Check the running system (adapt the curl port if `.env` overrides it):

```bash
curl -i http://localhost:8000/health/ready
docker compose run --rm --no-deps -e SMOKE_BASE_URL=http://api:8000 api pytest -q tests/smoke
```

The smoke test creates a synthetic case in PostgreSQL and waits for the worker
and AI service to complete it. The unit/integration tests use isolated SQLite
databases and do not modify the running application's data.

### Observed verification, 21 September 2026

Checks were executed by Codex in my local Docker environment:

| Check | Result |
| --- | --- |
| API image build | Successful |
| Unit and integration suite | 5 passed, 2 dependency deprecation warnings |
| Ruff | All checks passed |
| Running API readiness | HTTP 200, `{"service":"api","status":"ok"}` |
| Running-stack smoke test | 1 passed, 2 dependency deprecation warnings |
| Wrong-status regression probe | Changing the missing-job response from 404 to 400 caused the new test to fail |
| Wrong-message regression probe | Changing the detail to `Wrong message` caused the new test to fail |

Both regression probes changed only a disposable container's copy of the API
file; they did not modify the repository or running services. They demonstrate
that the assertions detect meaningful regressions, not just that the test runs.

## 4. Known limitations or notes

- This is one missing-job response test, not exhaustive API or concurrency testing.
- Integration tests use SQLite; PostgreSQL and asynchronous processing are
  additionally exercised by the separate smoke test.
- The starter contains `tests/integration/test_api_integration.py python`.
  Its suffix prevents normal pytest collection. It is unchanged and is not
  counted in the five passing tests; renaming it is outside this bounded change.
- Existing warnings concern Starlette/AnyIO and python-json-logger deprecations.
- Verification above used the current local checkout and Docker environment;
  it is not a claim that a fresh clone was independently tested.
- The private repository must be accessible to the designated course reviewers.

## 5. AI Use Statement

I used OpenAI Codex to explain the assignment, inspect the repository, draft the
missing-job test and this documentation, execute verification commands, and
prepare the Git/Canvas submission materials. I previously ran the classroom
startup, case-flow and baseline test commands and shared their outputs. For
this submission, Codex ran the five-test regression suite, lint, the live-stack
smoke test, and temporary regression probes. Those checks verified the status
and message assertions and that the existing flow still worked. Production API
behavior was left unchanged, and broader cleanup of the unusually named starter
test file was deferred. I do not claim that the AI-assisted code or documentation
was written independently or that I personally reran the agent's final checks.
