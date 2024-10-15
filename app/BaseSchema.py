from pydantic import BaseModel, ConfigDict
from typing import Any



class Model(BaseModel):
    
    model_config = ConfigDict(frozen = True, from_attributes = True, extra = 'ignore')
    
    
    def model_dump(self, **kwargs) -> dict[str, Any]:
        return super().model_dump(**kwargs, by_alias = True)
    
    
    