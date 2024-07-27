import os
import pickle
from types import SimpleNamespace
from pathlib import Path
from typing import Any, Callable, Optional, List
import functools
from globals import IS_DEBUG


def cached_call(func: Callable[..., Any]) -> Callable[..., Callable[..., Any]]:
    @functools.wraps(func)
    def cached_internal(cache_filename: str, params_list: Optional[List[str]] = None) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if IS_DEBUG:
                filename = Path(os.getcwd()) / "cache" / cache_filename
                cached_data = load_cached_data(filename)
               
                if cached_data is not None:
                    if not params_list:
                        return cached_data
                    elif isinstance(cached_data, SimpleNamespace):
                        # Check if all requested attributes are present
                        if all(hasattr(cached_data, attr) for attr in params_list):
                            filtered_cached = SimpleNamespace()
                            for attr in params_list:
                                setattr(filtered_cached, attr, getattr(cached_data, attr))
                            return filtered_cached
                        # If any attribute is missing, we'll call the function again
                    else:
                        raise ValueError("Cached data is not a SimpleNamespace object, but params_list is provided.")

            # Call the function if there's no valid cached data
            result = func(*args, **kwargs)

            if IS_DEBUG:
                if not params_list:
                    save_cached_data(filename, result)
                else:
                    filtered_result = SimpleNamespace()
                    for attr in params_list:
                        if hasattr(result, attr):
                            setattr(filtered_result, attr, getattr(result, attr))
                    save_cached_data(filename, filtered_result)

            if params_list:
                filtered_result = SimpleNamespace()
                for attr in params_list:
                    if hasattr(result, attr):
                        setattr(filtered_result, attr, getattr(result, attr))
                return filtered_result
            else:
                return result

        return wrapper
    return cached_internal

# Your existing cache functions remain unchanged
def load_cached_data(filename: Path) -> Optional[Any]:
    """Load cached data from a file."""
    filename = Path(filename)
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, pickle.UnpicklingError):
        return None

def save_cached_data(filename: Path, data: Any):
    """Save data to a cache file."""
    filename = Path(filename)
    if not filename.parent.exists():
        filename.parent.mkdir(parents=True)
    with open(filename, "wb") as file:
        pickle.dump(data, file)


def clear_cache(cache_filename: str) -> None:
    """
    Remove the specified cache file to clear the cache.

    Args:
    cache_filename (str): The name of the cache file to be removed.

    Returns:
    None

    Raises:
    FileNotFoundError: If the cache file doesn't exist.
    PermissionError: If there's no permission to delete the file.
    """
    try:
        cache_path = Path(os.getcwd()) / "cache" / cache_filename
        if cache_path.exists():
            cache_path.unlink()
            print(f"Cache file '{cache_filename}' has been successfully removed.")
        else:
            print(f"Cache file '{cache_filename}' does not exist.")
    except PermissionError:
        print(f"Permission denied: Unable to remove cache file '{cache_filename}'.")
    except Exception as e:
        print(f"An error occurred while trying to remove cache file '{cache_filename}': {str(e)}")

# Example usage:
# clear_cache("sample_probable_causation.pickle")

    