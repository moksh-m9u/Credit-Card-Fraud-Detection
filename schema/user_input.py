from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional

important_features=['V14', 'V10', 'V12', 'V4', 'V17', 'V3', 'V11', 'V16']

class user_input(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    # Required important features
    V14: Annotated[float, Field(..., description='Principal Component Analysis(PCA) component 14')] 
    V10: Annotated[float, Field(..., description='Principal Component Analysis(PCA) component 10')] 
    V12: Annotated[float, Field(..., description='Principal Component Analysis(PCA) component 12')] 
    V4: Annotated[float, Field(..., description='Principal Component Analysis(PCA) component 4')] 
    V17: Annotated[float, Field(..., description='Principal Component Analysis(PCA) component 17')] 
    V3: Annotated[float, Field(..., description='Principal Component Analysis(PCA) component 3')] 
    V11: Annotated[float, Field(..., description='Principal Component Analysis(PCA) component 11')] 
    V16: Annotated[float, Field(..., description='Principal Component Analysis(PCA) component 16')] 
    Amount: Annotated[float, Field(..., ge=0, description='Amount transferred')] 
    
    # Optional features
    V1: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 1')
    V2: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 2')
    V5: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 5')
    V6: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 6')
    V7: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 7')
    V8: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 8')
    V9: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 9')
    V13: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 13')
    V15: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 15')
    V18: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 18')
    V19: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 19')
    V20: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 20')
    V21: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 21')
    V22: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 22')
    V23: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 23')
    V24: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 24')
    V25: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 25')
    V26: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 26')
    V27: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 27')
    V28: Optional[float] = Field(None, description='Principal Component Analysis(PCA) component 28')
    Time: Optional[float] = Field(None, description='Seconds elapsed between each transaction and the first transaction in the dataset')



