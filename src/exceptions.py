class CustomAppException(Exception):
    def __init__(self, original_exception=None):
        super().__init__()
        self.original_exception = original_exception

class ProductNotFoundError(CustomAppException):
    def __init__(self, barcode_or_id=None, original_exception=None):
        super().__init__(f'The record belonging to the barcode or ID "{barcode_or_id}" could not be found in the database.\nOriginal exception: {original_exception}')
        self.barcode_or_id = barcode_or_id

class TransactionIntegrityError(CustomAppException):
    def __init__(self, original_exception=None):
        super().__init__(f"An error related to the integrity of the transaction occurred: {original_exception}")

class DBError(CustomAppException):
    def __init__(self, original_exception=None):
        super().__init__(f"Database Error: {original_exception}")