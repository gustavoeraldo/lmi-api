
class MeasurementsDescriptions:
    @staticmethod
    def description(endpoint: str):
        descriptions = {
            "get_all_measurements":"""Retrieves multiple measurement data.""",
            "add_measurement": """Add a new measurement to the database.""",
            }

        return descriptions[endpoint]
