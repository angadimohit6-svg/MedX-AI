class MeasurementProvider:
    def get_measurement(self, result): raise NotImplementedError
    def get_pixel_dimensions(self, result): raise NotImplementedError
    def get_physical_dimensions(self, result): raise NotImplementedError
    def get_area(self, result): raise NotImplementedError
