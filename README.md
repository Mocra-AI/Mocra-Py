# Mocra Python SDK

Python SDK for [Mocra's Observe API](https://docs.mocra.io/) — observability for video generation workflows. The API mirrors the [TypeScript SDK](https://github.com/Mocra-AI/Mocra) so you can switch between languages easily.

## Installation

```bash
pip install -e .
```

## Requirements

- Python 3.10+
- [httpx](https://www.python-httpx.org/)
- [pydantic](https://docs.pydantic.dev/) v2

## Quick Start

```python
from mocra import VideoObservabilityApi, ExtraCriterion

api = VideoObservabilityApi("YOUR_API_KEY")
result = api.score_video(
    "https://example.org/video.mp4",
    extra_criteria=[
        ExtraCriterion(
            criterion_name="Blur",
            criterion_description="The video should not be blurry",
        ),
    ],
    ignore_criteria=["UNNATURAL PHYSICS"],
)

print(f"Overall score: {result.severity}")
for criterion in result.criteria:
    print(f"  {criterion.name}: {criterion.score}")
```

## API Mapping (TypeScript ↔ Python)

| TypeScript | Python |
|------------|--------|
| `VideoObservabilityApi` | `VideoObservabilityApi` |
| `scoreVideo(videoUrl, extraCriteria?, ignoreCriteria?)` | `score_video(video_url, extra_criteria?, ignore_criteria?)` |
| `ExtraCriterion { criterionName, criterionDescription }` | `ExtraCriterion(criterion_name=..., criterion_description=...)` |
| `ignoreCriteria: ["UNNATURAL PHYSICS", ...]` | `ignore_criteria=["UNNATURAL PHYSICS"]` or `[DefaultCriterion.UNNATURAL_PHYSICS]` |
| `ScoreMap { severity, criteria }` | `ObserveResponse` |

**Default criteria** (for `ignore_criteria`): `UNNATURAL PHYSICS`, `MORPHING`, `FLICKERING`, `ARTIFACTING`, `TEXT ISSUES`

## API Reference

### VideoObservabilityApi

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | `str` | Your Mocra API key ([get one](https://docs.mocra.io/quickstart)) |
| `base_url` | `str` | Override API URL (default: `https://api.mocra.io`) |
| `timeout` | `float` | Request timeout in seconds |
| `http_client` | `httpx.Client` | Optional pre-configured client |

### score_video()

| Parameter | Type | Description |
|-----------|------|-------------|
| `video_url` | `str` | URL of the video to analyze |
| `extra_criteria` | `list[ExtraCriterion]` | Extra criteria (default: `[]`) |
| `ignore_criteria` | `list[str \| DefaultCriterion]` | Default criteria to exclude (default: `[]`) |

**Returns:** `{ severity, criteria: [{ name, score }] }` (1–100 scale)

## Context Manager

```python
with VideoObservabilityApi("YOUR_API_KEY") as api:
    result = api.score_video("https://example.org/video.mp4")
```

## Development

### Setup

```bash
pip install -e ".[dev]"
pre-commit install  # Run lint on git commit
```

### Lint

```bash
ruff check mocra tests
```

### Test

```bash
pytest tests/ -v
```

### Publishing to PyPI

1. Create an API token at [pypi.org/manage/account/token](https://pypi.org/manage/account/token)
2. Add `PYPI_API_TOKEN` as a repository secret in GitHub
3. Create a release or run the workflow manually — the publish workflow runs on release publish and `workflow_dispatch`

## License

MIT
