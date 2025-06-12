class TestCoordinatorInterface:
    """測試協調器接口定義"""
    def initialize(self):
        raise NotImplementedError
    
    def get_status(self):
        raise NotImplementedError


