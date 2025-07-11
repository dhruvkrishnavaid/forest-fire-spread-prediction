from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.fire_prediction import FirePredictionRequest, FirePredictionResponse
from app.services.ml_models import FirePredictionService
from app.services.data_processing import DataProcessor
import uuid

router = APIRouter()

@router.post("/predict", response_model=FirePredictionResponse)
async def predict_fire_probability(
    request: FirePredictionRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate fire probability map for next day
    """
    try:
        # Initialize services
        data_processor = DataProcessor()
        ml_service = FirePredictionService()
        
        # Process input data
        processed_data = await data_processor.prepare_prediction_data(
            bounds=request.region_bounds,
            weather=request.weather_data,
            date=request.prediction_date
        )
        
        # Generate prediction
        prediction_result = await ml_service.predict_fire_probability(processed_data)
        
        # Generate unique filename for raster output
        output_filename = f"fire_prediction_{uuid.uuid4().hex}.tif"
        
        # Save raster file in background
        background_tasks.add_task(
            ml_service.save_prediction_raster,
            prediction_result,
            output_filename
        )
        
        return FirePredictionResponse(
            prediction_map_url=f"/outputs/rasters/{output_filename}",
            risk_zones=prediction_result["risk_zones"],
            overall_risk_level=prediction_result["overall_risk"],
            confidence_score=prediction_result["confidence"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regions")
async def get_available_regions():
    """
    Get list of available regions for prediction
    """
    return {
        "regions": [
            {"name": "Uttarakhand", "bounds": [[28.43, 77.34], [31.45, 81.03]]},
            {"name": "Himachal Pradesh", "bounds": [[30.22, 75.47], [33.23, 79.04]]},
            # Add more regions as needed
        ]
    }
