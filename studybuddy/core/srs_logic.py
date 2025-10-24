# In studybuddy/core/srs_logic.py

from datetime import datetime, timedelta, timezone
from studybuddy.database.models import Flashcard

def calculate_srs_update(flashcard: Flashcard, performance_rating: int) -> Flashcard:
    """
    Updates a flashcard's SRS metadata based on user performance.
    
    Args:
        flashcard (Flashcard): The flashcard object from the database.
        performance_rating (int): A rating of how well the user remembered (e.g., 0-5).
                                 For our MVP, we'll use a simpler system:
                                 - 1 = Failed (e.g., "Hard / Again")
                                 - 3 = Recalled with some difficulty (e.g., "Good")
                                 - 5 = Recalled easily (e.g., "Easy")
    Returns:
        The updated, but not yet committed, flashcard object.
    """
    if performance_rating < 3: # User failed to recall
        # Reset interval to start over
        flashcard.interval = 1
    else: # User recalled correctly
        if flashcard.reviews == 0:
            flashcard.interval = 1
        elif flashcard.reviews == 1:
            flashcard.interval = 6
        else:
            new_interval = flashcard.interval * flashcard.ease_factor
            flashcard.interval = round(new_interval)

    # Update the ease factor based on performance
    # Formula is based on SM-2 algorithm
    new_ease = flashcard.ease_factor + (0.1 - (5 - performance_rating) * (0.08 + (5 - performance_rating) * 0.02))
    # Keep ease factor from dropping too low
    flashcard.ease_factor = max(1.3, new_ease)
    
    # Increment the review count
    flashcard.reviews += 1
    
    # Set the next review date
    flashcard.next_review_at = datetime.now(timezone.utc) + timedelta(days=flashcard.interval)
    
    return flashcard