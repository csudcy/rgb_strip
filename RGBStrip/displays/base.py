class BaseDisplay(object):
    def __init__(self, controller):
        self.CONTROLLER = controller

    def display(self):
        raise Exception('Inheriting classes must override BaseDisplay.display!')

    def setup(self):
        """
        Put any context setup logic here
        """
        pass

    def teardown(self):
        """
        Put any context teardown logic here
        """
        pass

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.teardown()