class BaseDisplay(object):
    def __init__(self, controller):
        self.CONTROLLER = controller

    def display(self):
        raise Exception('Inheriting classes must override BaseDisplay.display!')

    def safe_setup(self):
        try:
            self.setup()
            self.SETUP_DONE = True
        except Exception, ex:
            logging.error('Exception during setup: %s', str(ex))

    def setup(self):
        """
        Put any context setup logic here
        """
        pass

    def safe_teardown(self):
        if self.SETUP_DONE:
            try:
                self.teardown()
            except Exception, ex:
                logging.error('Exception during teardown: %s', str(ex))
            self.SETUP_DONE = False

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
