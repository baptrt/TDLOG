from typing import Protocol

"""
This module provides an implementation of the observer pattern
(See for instance https://en.wikipedia.org/wiki/Observer_pattern).
"""


class Observer[T](Protocol):

    def update(self, old_value: T, new_value: T) -> None:
        """
        Method called to notify the observer that the subject has been
        updated, passing the subject values before and after modification.
        """
        ...


class Subject[T](Protocol):
    def add_observer(self, observer: Observer[T]) -> None:
        """
        Registers the passed observer so that it will be notified of
        subsequent subject changes. Does nothing if `observer` has
        already been registered.
        """
        ...

    def remove_observer(self, observer: Observer[T]) -> None:
        """
        Unregisters the passed observer so that it will no longer be
        notified about subject changes. Does nothing if `observer` is
        not registered.
        """
        ...

    def notify_observers(self, old_value: T, new_value: T) -> None:
        """
        Notify the currently-registered observers that the subject
        value has changed from `old_value` to `new_value`.
        """
        ...



# Concrete Subject implementation
class SubjectClass[T]:
    def __init__(self) -> None:
        self._observers: list[Observer[T]] = []  # Stores registered observers

    # Add observer if not already registered
    def add_observer(self, observer: Observer[T]) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    # Remove observer if present
    def remove_observer(self, observer: Observer[T]) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    # Notify all observers of a value change
    def notify_observers(self, old_value: T, new_value: T) -> None:
        for observer in self._observers:
            observer.update(old_value, new_value)
            
    # Change the subject’s value and notify observers
    def change_value(self, old_value: T, new_value: T) -> None:
        self.notify_observers(old_value, new_value)
    

# Concrete Observer: prints change in English
class EnglishObserverClass[T]:
    def update(self, old_value: T, new_value: T) -> None:
        print(f"Value changed from {old_value} to {new_value}")
        

# Concrete Observer: prints change in French
class FrenchObserverClass[T]:
    def update(self, old_value: T, new_value: T) -> None:
        print(f"La valeur a changé de {old_value} à {new_value}")
