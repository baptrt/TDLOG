from observer import SubjectClass, EnglishObserverClass, FrenchObserverClass

# Create a subject (manages observers and notifies them)
my_subject = SubjectClass[int]()

# Create two observers
my_first_observer = FrenchObserverClass[int]()
my_second_observer = EnglishObserverClass[int]()

# First change (no observers yet, nothing happens)
print("=== Change 1 ===")
my_subject.change_value(0, 123)

# Add both observers
my_subject.add_observer(my_first_observer)
my_subject.add_observer(my_second_observer)

# Second change (both observers are notified)
print("=== Change 2 ===")
my_subject.change_value(123, 456)

# Remove the French observer
my_subject.remove_observer(my_first_observer)

# Third change (only English observer is notified)
print("=== Change 3 ===")
my_subject.change_value(456, 789)
