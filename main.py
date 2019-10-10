import sys

from lib.ResponseBuilder.ResponseBuilder import ResponseBuilder
from lib.ResultsDisplay.ResultsDisplay import ResultsDisplay
from lib.Validation.Validator import Validator as val


def main():
    """
    App main method.
    """

    # Abort program execution if input validation fails
    if val.validate() is not True: sys.exit()

    # Build response JSON
    response = ResponseBuilder.build(val.get_data_source(), val.get_date_filter())

    # Display results
    ResultsDisplay.show(response)


if __name__ == "__main__":
    main()