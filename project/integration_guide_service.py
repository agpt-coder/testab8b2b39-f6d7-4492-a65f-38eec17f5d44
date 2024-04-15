from typing import Dict, List

from prisma import Prisma
from pydantic import BaseModel


class IntegrationGuideResponse(BaseModel):
    """
    Response model containing the requested documentation and integration guides for the specified third-party service.
    """

    service_name: str
    documentation_url: str
    integration_steps: List[str]
    sdk_support: Dict[str, str]


async def integration_guide(service_name: str) -> IntegrationGuideResponse:
    """
    Retrieves integration guides and documentation for third-party services.

    Args:
        service_name (str): The unique name or identifier of the third-party service for which the documentation is requested.

    Returns:
        IntegrationGuideResponse: Response model containing the requested documentation and integration guides for the specified third-party service.
    """
    module = await Prisma.module.find_unique(
        where={"name": service_name}, include={"features": True}
    )
    if not module:
        raise ValueError(f"No integration guide found for service '{service_name}'")
    documentation_url = (
        f"https://{service_name.lower().replace(' ', '-')}.docs.example.com"
    )
    integration_steps = [
        "Sign up for an API Key",
        "Configure API settings",
        "Start integrating API endpoints",
    ]
    sdk_support = {
        "Python": "https://pypi.org/project/{service_name}/",
        "JavaScript": "https://npmjs.com/package/{service_name}/",
    }
    return IntegrationGuideResponse(
        service_name=service_name,
        documentation_url=documentation_url,
        integration_steps=integration_steps,
        sdk_support=sdk_support,
    )
