
### `API_DOCS.md`

```markdown
Recommendation Service API Documentation

Overview
API documentation for the Recommendation Service, which provides product recommendations based on user interactions.

Version: 1.0.0
API Specification: OpenAPI 3.1

Endpoints

Recommendation Endpoints

Get Recommendations
- URL: /api/v1/recommendations/{user_id}
- Method: GET
- Summary: Retrieve product recommendations for a specific user.
- Parameters:
  - user_id (integer): The ID of the user.
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/RecommendationResponseSchema"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get Recommendations Collaborative
- URL: /api/v1/recommendations/collaborative/{user_id}
- Method: GET
- Summary: Retrieve collaborative filtering recommendations for a specific user.
- Parameters:
  - user_id (integer): The ID of the user.
- Response:
  - 200 Successful Response:
    {
      "type": "array",
      "items": {
        "$ref": "#/components/schemas/ProductSchema"
      }
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get Recommendations Content
- URL: /api/v1/recommendations/content/{user_id}
- Method: GET
- Summary: Retrieve content-based filtering recommendations for a specific user.
- Parameters:
  - user_id (integer): The ID of the user.
- Response:
  - 200 Successful Response:
    {
      "type": "array",
      "items": {
        "$ref": "#/components/schemas/ProductSchema"
      }
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get Recommendations Hybrid
- URL: /api/v1/recommendations/hybrid/{user_id}
- Method: GET
- Summary: Retrieve hybrid filtering recommendations for a specific user.
- Parameters:
  - user_id (integer): The ID of the user.
- Response:
  - 200 Successful Response:
    {
      "type": "array",
      "items": {
        "$ref": "#/components/schemas/ProductSchema"
      }
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get Vendor Recommendations
- URL: /api/v1/vendor-recommendations/{user_id}
- Method: GET
- Summary: Retrieve vendor recommendations for a specific user.
- Parameters:
  - user_id (integer): The ID of the user.
- Response:
  - 200 Successful Response:
    {
      "type": "array",
      "items": {
        "$ref": "#/components/schemas/VendorSchema"
      }
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get TF Recommendations
- URL: /api/v1/recommendations/tfrs/{user_id}
- Method: GET
- Summary: Retrieve TensorFlow-based recommendations for a specific user.
- Parameters:
  - user_id (string): The ID of the user.
- Response:
  - 200 Successful Response
    {}
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Miscellaneous Endpoints

Create Dummy Data
- URL: /api/v1/create_dummy_data/
- Method: POST
- Summary: Create dummy data for testing purposes.
- Response:
  - 200 Successful Response
    {}

Read Root
- URL: /
- Method: GET
- Summary: Root endpoint.
- Response:
  - 200 Successful Response
    {}
