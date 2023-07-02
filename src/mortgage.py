import argparse


def get_equivalent_periodic_rate(interest_rate: float, periods: int) -> float:
    """
    Calculate the equivalent periodic interest rate.

    The equivalent periodic interest rate is the interest rate that is
    equivalent to the effective annual interest rate. It is calculated
    as follows:

        r = (1 + i) ** (1 / n) - 1

    Arguments:
        interest_rate (float): The interest rate.

    Returns:
        float: The equivalent periodic interest rate.
    """
    return (1 + interest_rate) ** (1 / periods) - 1


def evaluate_annuity(payment: float, interest_rate: float, periods: int) -> float:
    """
    Evaluate an annuity given the payment, interest rate and periods.

    An annuity is a series of payments made at equal intervals for a
    fixed duration. Examples of annuities are regular deposits to a savings
    account, monthly home mortgage payments, monthly insurance payments and
    pension payments.

    Arguments:
        payment (float): The payment amount.
        interest_rate (float): The interest rate.
        periods (int): The number of periods.

    Returns:
        float: The annuity value, in the same unit as the payment.
    """
    return (payment / interest_rate) - (payment / interest_rate) / (
        (1 + interest_rate) ** periods
    )


def get_annuity_payment(
    annuity_value: float, interest_rate: float, periods: int
) -> float:
    """
    Calculate the annuity payment. The annuity payment is the amount of
    money that is paid to the lender at a specified time interval for a
    fixed number of intervals. The annuity payment formula is derived
    from the annuity formula as follows:

        V = (C / r) - (C / r) / (1 + r) ** T
        => V * r = C - C / (1 + r) ** T
        => V * r = C * (1 - 1 / (1 + r) ** T)
        => C = V * r / (1 - 1 / (1 + r) ** T)

    Arguments:
        annuity_value (float): The annuity value.
        interest_rate (float): The interest rate.
        periods (int): The number of periods.

    Returns:
        float: The annuity payment.
    """
    return annuity_value * interest_rate / (1 - 1 / (1 + interest_rate) ** periods)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate the annuity payment for a mortgage."
    )
    parser.add_argument(
        "--amount", type=float, help="The principal amount of the mortgage."
    )
    parser.add_argument(
        "--interest-rate",
        type=float,
        help="The yearly interest rate as a decimal (e.g., 0.05 for 5%).",
    )
    parser.add_argument("--years", type=int, help="The number of years.")
    parser.add_argument(
        "--compounding-periods",
        type=int,
        help="The number of compounding periods in a year.",
    )
    args = parser.parse_args()

    # get effective yearly interest rate
    equivalent_periodic_rate = get_equivalent_periodic_rate(
        args.interest_rate, args.compounding_periods
    )
    print("Equivalent periodic rate: {:.8%}".format(equivalent_periodic_rate))

    total_periods = args.years * args.compounding_periods

    payment = get_annuity_payment(
        args.amount,
        equivalent_periodic_rate,
        total_periods,
    )
    print("Monthly payment: {:.2f}".format(payment * args.compounding_periods / 12))


if __name__ == "__main__":
    main()
