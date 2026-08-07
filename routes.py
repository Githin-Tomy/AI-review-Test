# routes.py
from fastapi import APIRouter, HTTPException, status
from main import get_user_by_username, delete_user, search_products

# Initialize the router
router = APIRouter(prefix="/api", tags=["app"])

@router.get("/users/{username}")
def fetch_user(username: str):
    """Fetch a user profile by username."""
    user = get_user_by_username(username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User '{username}' not found."
        )
        
    return {"status": "success", "data": user}


@router.delete("/users/{user_id}")
def remove_user(user_id: str):
    """Delete a user by their ID."""
    success = delete_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found or already deleted."
        )
        
    return {"status": "success", "message": "User deleted successfully."}


@router.get("/products/search")
def search_inventory(query: str):
    """Search for products by name."""
    
    # ⚠️ This is the downstream call for your AI to test.
    # It passes exactly 1 argument (query) to search_products.
    results = search_products(query)
    
    return {
        "status": "success", 
        "count": len(results),
        "data": results
    }