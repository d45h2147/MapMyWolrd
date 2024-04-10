from mapmyworld.extensions import api
from mapmyworld.resource import categories, locations, location_category_reviewed, explore_recommendation

api.add_resource(locations.RestLocation, "/api/v1/locations")
api.add_resource(categories.RestCategories, "/api/v1/categories")
api.add_resource(location_category_reviewed.RestLocationCategoryReviewed, "/api/v1/locationCategoryReviewed")
api.add_resource(explore_recommendation.RestExploreRecommendation, "/api/v1/exploreRecommendation")
