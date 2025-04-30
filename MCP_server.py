from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from . import models, schemas, crud
from .database import get_db

# Create a separate FastAPI app for the MCP server
mcp_app = FastAPI(
    title="Thailand Travel MCP Server",
    description="MCP Server for recommending travel itineraries in Thailand",
    version="1.0.0"
)

class RecommendationRequest(BaseModel):
    num_nights: int = Field(..., ge=1, le=14)
    regions: Optional[str] = None
    budget: Optional[float] = None
    preferences: Optional[List[str]] = None  # e.g., ["beach", "adventure", "luxury"]

class RecommendationResponse(BaseModel):
    itineraries: List[schemas.Itinerary]
    message: str

@mcp_app.post("/recommend/", response_model=RecommendationResponse)
def recommend_itineraries(request: RecommendationRequest, db: Session = Depends(get_db)):
    """
    Recommend itineraries based on the number of nights, regions, budget, and preferences.
    
    This endpoint serves as the MCP (Master Control Program) for the recommendation system.
    It analyzes the user's requirements and returns the most suitable itineraries.
    """
    # Get base recommendations from the database
    itineraries = crud.get_recommended_itineraries(
        db, 
        num_nights=request.num_nights, 
        regions=request.regions,
        budget=request.budget
    )
    
    # If no itineraries found, try to find closest matches
    if not itineraries:
        # Try with +/- 1 night
        alternative_nights = [request.num_nights - 1, request.num_nights + 1]
        for nights in alternative_nights:
            if nights > 0:
                alternative_itineraries = crud.get_recommended_itineraries(
                    db, 
                    num_nights=nights, 
                    regions=request.regions,
                    budget=request.budget
                )
                if alternative_itineraries:
                    return {
                        "itineraries": alternative_itineraries,
                        "message": f"No exact matches found for {request.num_nights} nights. Showing alternatives with {nights} nights."
                    }
        
        # If still no matches, try without budget constraint
        if request.budget:
            no_budget_itineraries = crud.get_recommended_itineraries(
                db, 
                num_nights=request.num_nights, 
                regions=request.regions,
                budget=None
            )
            if no_budget_itineraries:
                return {
                    "itineraries": no_budget_itineraries,
                    "message": f"No itineraries found within your budget of {request.budget}. Showing alternatives that may exceed your budget."
                }
        
        # If still no matches, try without region constraint
        if request.regions:
            no_region_itineraries = crud.get_recommended_itineraries(
                db, 
                num_nights=request.num_nights, 
                regions=None,
                budget=request.budget
            )
            if no_region_itineraries:
                return {
                    "itineraries": no_region_itineraries,
                    "message": f"No itineraries found for the specified regions. Showing alternatives from all regions."
                }
        
        # Last resort: return any recommended itineraries
        any_itineraries = crud.get_recommended_itineraries(db, num_nights=0, regions=None, budget=None)
        if any_itineraries:
            return {
                "itineraries": any_itineraries[:5],  # Limit to 5 results
                "message": "No exact matches found. Showing our most popular itineraries."
            }
        
        # If absolutely nothing found
        raise HTTPException(status_code=404, detail="No itineraries found matching your criteria or alternatives.")
    
    # Apply preference-based ranking if preferences are provided
    if request.preferences and itineraries:
        # This is a simple implementation - in a real system, you would use more sophisticated ranking
        scored_itineraries = []
        for itinerary in itineraries:
            score = 0
            # Check if preferences match regions, description, or activities
            for preference in request.preferences:
                preference = preference.lower()
                if preference in itinerary.regions.lower():
                    score += 3
                if itinerary.description and preference in itinerary.description.lower():
                    score += 2
                
                # Check activities (this requires loading the days)
                for day in itinerary.days:
                    for activity in day["activities"]:
                        if preference in activity.name.lower() or (activity.description and preference in activity.description.lower()):
                            score += 1
            
            scored_itineraries.append((score, itinerary))
        
        # Sort by score (descending)
        scored_itineraries.sort(reverse=True, key=lambda x: x[0])
        
        # Extract just the itineraries
        itineraries = [item[1] for item in scored_itineraries]
    
    return {
        "itineraries": itineraries,
        "message": f"Found {len(itineraries)} itineraries matching your criteria."
    }

# Run the MCP server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp_app, host="0.0.0.0", port=8001)
