#!/usr/bin/env python3
"""
Quickstart example - mirrors TypeScript SDK usage.

Usage:
    export MOCRA_API_KEY="your-api-key"
    python examples/quickstart.py

TypeScript equivalent:
    new VideoObservabilityApi(apiKey).scoreVideo(videoUrl, extraCriteria, ignoreCriteria)
"""

import os

from mocra import VideoObservabilityApi, ExtraCriterion


def main() -> None:
    api_key = os.environ.get("MOCRA_API_KEY")
    if not api_key:
        print("Set MOCRA_API_KEY environment variable")
        return

    api = VideoObservabilityApi(api_key)
    result = api.score_video(
        "https://example.org/video.mp4",  # Replace with your video URL
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


if __name__ == "__main__":
    main()
