from ..dice import Die
import pytest

@pytest.mark.parametrize('n', (6, 7, 8))
def test_valid_roll(n):
    """ Test that a die roll is valid. """

    # Intialise a standard, six-sided die.
    die = Die(n=n)

    # Roll the die.
    roll = die.roll()

    # Check that the value is valid.
    assert roll > 0 and roll < n + 1


def test_always_valid_roll():
    """ Test that a die roll is "always" valid. """

    # Intialise a standard, six-sided die.
    die = Die()

    # Roll the die lots of times.
    for i in range(10000):
        roll = die.roll()

        # Check that the value is valid.
        assert roll > 0 and roll < 7


def test_average():
    """ Test that the average die roll is correct. """

    # Intialise a standard, six-sided die.
    die = Die()

    # Work out the expected average roll.
    expect = sum(range(1, 7)) / 6

    # Calculate the sum of the die rolls.
    total = 0
    
    # Set the number of rolls.
    rolls = 100000

    for i in range(0, rolls):
        total += die.roll()

    # Check that the average matches the expected value.
    average = total / rolls
    assert average == pytest.approx(3.5, rel=1e-2)


def test_fair():
    """ Test that a die is fair. """

    # Intialise a standard, six-sided die.
    die = Die()

    # Set the number of rolls.
    rolls = 1000000

    # Create a dictionary to hold the tally for each outcome.
    tally = {}
    for i in range(1, 7):
        tally[i] = 0

    # Roll the die 'rolls' times.
    for i in range(0, rolls):
        tally[die.roll()] += 1

    # Assert that the probability is correct.
    for i in range(1, 7):
        assert tally[i] / rolls == pytest.approx(1 / 6, 1e-2)


def test_double_roll():
    # Store the expected probabilities for the sum of two dice.
    expect = {}
    for x in range(2, 13):
        expect[x] = prob_double_roll(x, 6)

    # Create a dictionary to hold the tally for each outcome.
    tally = {}
    for key in expect:
        tally[key] = 0

    # Initialise the die.
    die = Die(6)

    # Roll two dice 'rolls' times.
    rolls = 5000000
    for i in range(0, rolls):

        # Sum the value of the two dice rolls.
        roll_sum = die.roll() + die.roll()

        # Increment the tally for the outcome.
        tally[roll_sum] += 1

    # Compute the probabilities and check with expected values.
    for key in tally:

        average = tally[key] / rolls
        assert average == pytest.approx(expect[key], rel=1e-2)


def prob_double_roll(x, n):
    """
    Expected probabilities for the sum of two dice.
    """
    # For two n-sided dice, the probability of two rolls summing to x is
    # (n − |x−(n+1)|) / n^2, for x = 2 to 2n.

    return (n - abs(x - (n + 1))) / n ** 2
