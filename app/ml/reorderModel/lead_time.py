class LeadTimeCalculator:

    """
    Supplier Lead Time

    Future:
        Database
        Supplier API
        Nimbus
    """

    DEFAULT_DAYS = 7

    @classmethod
    def calculate(

        cls,

        category=None

    ):

        mapping = {

            "Gold": 10,

            "Silver": 7,

            "Artificial": 5

        }

        if category:

            for key in mapping:

                if key.lower() in category.lower():

                    return {

                        "leadTimeDays": mapping[key],

                        "source": key

                    }

        return {

            "leadTimeDays": cls.DEFAULT_DAYS,

            "source": "Default"

        }