from collections import Counter
from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class UserBehaviorResponse(BaseModel):
    """
    Response model containing analyzed data of user behavior.
    """

    user_id: str
    overall_interaction_count: int
    most_active_time_slot: str
    top_interactions: List[str]


async def user_behavior(
    user_id: str, start_date: datetime, end_date: datetime
) -> UserBehaviorResponse:
    """
    Provides real-time analytics on user behavior patterns.

    This function fetches interactions and analytics data for a specific user within a provided time period and
    computes metrics such as the total interaction count, most active time slot, and top interaction types.

    Args:
        user_id (str): Unique identifier for the user to fetch analytics for.
        start_date (datetime): The starting date for the period to retrieve analytics.
        end_date (datetime): The ending date for the period to retrieve analytics.

    Returns:
        UserBehaviorResponse: Response model containing analyzed data of user behavior.

    Example:
        user_id = '123abc'
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 31)
        user_behavior_data = await user_behavior(user_id, start_date, end_date)
        print(user_behavior_data)
    """
    interactions = await prisma.models.UserModuleInteraction.prisma().find_many(
        where={"userId": user_id, "interactionAt": {"gte": start_date, "lte": end_date}}
    )
    interaction_counts = Counter(
        [interaction.moduleName for interaction in interactions]
    )
    total_interactions = sum(interaction_counts.values())
    if not interactions:
        return UserBehaviorResponse(
            user_id=user_id,
            overall_interaction_count=0,
            most_active_time_slot="No interaction in the period",
            top_interactions=[],
        )
    time_slots = {
        interaction.interactionAt.hour: interaction for interaction in interactions
    }
    most_active_hour = max(
        time_slots,
        key=lambda hour: sum(
            (
                1
                for interaction in interactions
                if interaction.interactionAt.hour == hour
            )
        ),
    )
    time_slot_mapping = {
        range(0, 6): "Midnight 12AM - 6AM",
        range(6, 12): "Morning 6AM - 12PM",
        range(12, 18): "Afternoon 12PM - 6PM",
        range(18, 24): "Evening 6PM - 12AM",
    }
    most_active_time_slot = next(
        (
            slot
            for time_range, slot in time_slot_mapping.items()
            if most_active_hour in time_range
        ),
        "Unknown",
    )
    top_interactions = [
        interaction for interaction, count in interaction_counts.most_common(3)
    ]
    return UserBehaviorResponse(
        user_id=user_id,
        overall_interaction_count=total_interactions,
        most_active_time_slot=most_active_time_slot,
        top_interactions=top_interactions,
    )
