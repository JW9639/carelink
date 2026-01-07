"""Bloodwork service for business logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.db.repositories.bloodwork_repository import BloodworkRepository
from app.models.bloodwork import Bloodwork


@dataclass
class MarkerSummary:
    """Summary counts for marker status."""

    total: int
    out_of_range: int


class BloodworkService:
    """Service for bloodwork-related business logic."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.bloodwork_repo = BloodworkRepository(db)

    def get_published_results(self, patient_id: int) -> list[Bloodwork]:
        """Return published bloodwork results for a patient."""
        return self.bloodwork_repo.get_published_for_patient(patient_id)

    def normalize_bloodwork(self, bloodwork: Bloodwork) -> dict[str, Any]:
        """Normalize bloodwork payloads into a common structure."""
        results = bloodwork.results or {}
        if isinstance(results, dict) and "categories" in results:
            return {
                "test_name": results.get("test_name") or bloodwork.test_type,
                "categories": results.get("categories", []),
            }

        markers = []
        reference_ranges = bloodwork.reference_ranges or {}
        for name, value in results.items():
            reference_range = self._parse_reference_range(reference_ranges.get(name))
            markers.append(
                {
                    "name": name,
                    "abbreviation": name,
                    "value": value,
                    "unit": "",
                    "reference_range": reference_range,
                }
            )
        return {
            "test_name": bloodwork.test_type,
            "categories": [{"name": "Results", "markers": markers}],
        }

    def summarize_categories(self, categories: list[dict[str, Any]]) -> MarkerSummary:
        """Return total markers and out-of-range count."""
        total = 0
        out_of_range = 0
        for category in categories:
            markers = category.get("markers", [])
            total += len(markers)
            for marker in markers:
                status = self.get_marker_status(marker)
                if status in {"low", "high", "critical"}:
                    out_of_range += 1
        return MarkerSummary(total=total, out_of_range=out_of_range)

    def summarize_category(self, category: dict[str, Any]) -> MarkerSummary:
        """Return summary for a single category."""
        markers = category.get("markers", [])
        total = len(markers)
        out_of_range = sum(
            1
            for marker in markers
            if self.get_marker_status(marker) in {"low", "high", "critical"}
        )
        return MarkerSummary(total=total, out_of_range=out_of_range)

    def get_marker_status(self, marker: dict[str, Any]) -> str:
        """Return a normalized marker status."""
        status = marker.get("status")
        if isinstance(status, str) and status:
            return status.lower()

        reference = marker.get("reference_range") or {}
        try:
            value = float(marker.get("value"))
        except (TypeError, ValueError):
            return "unknown"

        low = reference.get("low")
        high = reference.get("high")
        optimal_low = reference.get("optimal_low", low)
        optimal_high = reference.get("optimal_high", high)

        if low is None or high is None:
            return "unknown"

        try:
            low = float(low)
            high = float(high)
            if optimal_low is not None:
                optimal_low = float(optimal_low)
            if optimal_high is not None:
                optimal_high = float(optimal_high)
        except (TypeError, ValueError):
            return "unknown"

        if value < low or value > high:
            return "critical"
        if optimal_low is not None and value < optimal_low:
            return "low"
        if optimal_high is not None and value > optimal_high:
            return "high"
        return "normal"

    def _parse_reference_range(self, raw_range: Any) -> dict[str, float]:
        if isinstance(raw_range, dict):
            return raw_range
        if isinstance(raw_range, str):
            parts = raw_range.replace(" ", "").split("-")
            if len(parts) == 2:
                try:
                    low = float(parts[0])
                    high = float(parts[1])
                except ValueError:
                    return {}
                return {
                    "low": low,
                    "optimal_low": low,
                    "optimal_high": high,
                    "high": high,
                }
        return {}
