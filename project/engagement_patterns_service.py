from datetime import datetime
from typing import Any, Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class EngagementPatternsResponse(BaseModel):
    """
    Provides summarized data and insights into user engagement patterns within the specified period.
    """

    overview: str
    details: Dict[str, Any]
    recommendations: List[str]


async def engagement_patterns(
    start_date: datetime, end_date: datetime, segment: Optional[str] = None
) -> EngagementPatternsResponse:
    """
    Analyzes engagement patterns to offer insights for UX improvement.

    Args:
        start_date (datetime): Start date for the period to analyze engagement patterns.
        end_date (datetime): End date for the period to analyze engagement patterns.
        segment (Optional[str]): Optional user segment to filter the analysis.

    Returns:
        EngagementPatternsResponse: Provides summarized data and insights into user engagement patterns within the specified period.
    """
    where_segment = {}
    if segment:
        where_segment["user"] = {"role": {"equals": segment}}
    interactions = await prisma.models.UserModuleInteraction.prisma().find_many(
        where={
            "AND": [
                {"interactionAt": {"gte": start_date, "lte": end_date}},
                where_segment,
            ]
        }
    )
    module_names = [interaction.moduleName for interaction in interactions]
    unique_module_names = set(module_names)
    module_interaction_counts = {
        module: module_names.count(module) for module in unique_module_names
    }
    overview = "Engagement analysis for the selected period."
    details = {
        "total_interactions": len(interactions),
        "interactions_by_module": module_interaction_counts,
    }
    recommendations = [
        "Review modules with lower engagement for potential UX improvements.",
        "Consider additional features for modules with high engagement.",
    ]
    return EngagementPatternsResponse(
        overview=overview, details=details, recommendations=recommendations
    )
