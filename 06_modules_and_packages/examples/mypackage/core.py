"""
Core functionality for the mypackage package.
"""

from typing import List, Dict, Any, Optional
from .utils import validate_input, format_output
from .subpackage.helpers import helper_function


class DataProcessor:
    """Main class for processing data"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    def process(self, data: List[Any]) -> List[Any]:
        """Process a list of data items"""
        # Validate input
        if not validate_input(data):
            raise ValueError("Invalid input data")
        
        # Process data
        processed = []
        for item in data:
            result = self._process_item(item)
            processed.append(result)
        
        # Format output
        return format_output(processed)
    
    def _process_item(self, item: Any) -> Any:
        """Process a single item"""
        # Use helper function from subpackage
        return helper_function(item)


def process_data(data: List[Any], config: Optional[Dict[str, Any]] = None) -> List[Any]:
    """Convenience function for processing data"""
    processor = DataProcessor(config)
    return processor.process(data) 