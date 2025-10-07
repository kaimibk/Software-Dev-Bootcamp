# Week 3, Session 3: Writing Robust, Maintainable Code

In our previous sessions, you learned to write structured, well-organized code using object-oriented principles. Today, we're focusing on the practices that distinguish good code from great code: **robustness**, **readability**, and **maintainability**. We'll integrate these concepts into a continuous process, showing you how to transform "code smells" into professional, production-ready code.

-----

## The Starting Point: Code Smells

We'll use these two examples to guide our lesson. These patterns are common in rapid prototyping but lead to maintenance headaches:

  * **Code Smell 1: Ambiguous Logic and Return Types**

    ```python linenums="1"
    def do_it(x, y):  # (1)!
        z = x + y if x else y * 2
        if z > 100:
            return {"a": z}
        return z  # (2)!
    ```
    { .annotate }

    1. What are the inputs (`x`, `y`)? An `int`? A `str`?
    2. What are the outputs? It can return an `int`, or a `dict`, leading to confusion for anyone calling this function.
    <!-- end list -->


  * **Code Smell 2: Unstructured Data and Fragile Access**

    ```python linenums="1"
    def process(data):
        if (data["age"] > 18 and data["status"] == "active") or (data["access"]["level"] == "ADMIN"):  # (1)!
            return {"ok": True, "msg": "allowed"}
        return {"ok": False}
    ```
    { .annotate }

    1. This code assumes the input `data` (a dictionary) has the keys `age` (which is an integer) and `status` (which is a string). If any key is missing or the type is wrong, the code will crash at runtime.

    <!-- end list -->

-----

## Tool 1: Type Hints and Static Analysis (Fixing Ambiguity)

The first step in professional development is clarifying intent. **Type hints** tell developers and machines what types of data are expected, solving the ambiguity in **Code Smell 1**.

**Applying Type Hints**

1.  We start by clarifying the inputs to `do_it` are numbers, but we still have an ambiguous return type (`Union`).

2.  We introduce **Enums** and **Literals** to enforce highly specific input values, solving common logic bugs before they happen.

    ```python linenums="1"
    from typing import Literal, Union
    from enum import StrEnum

    # Use StrEnum for status to eliminate magic strings
    class UserStatus(StrEnum):
        ACTIVE = "active"
        INACTIVE = "inactive"
        SUSPENDED = "suspended"

    # Example: Use Literal to constrain the column name to specific strings
    def sort_data(column: Literal["date", "name"], direction: Literal["asc", "desc"]) -> None:
        pass

    # Applying to Code Smell 1 (conceptually):
    # This clarifies the input must be integers, but the output is complex.
    # The static checker (mypy) would immediately flag the inconsistent return types.
    def do_it_typed(x: int, y: int) -> Union[int, Dict[str, int]]:
        # ... logic
        pass
    ```

**Static Analysis:** After adding type hints, we run **`mypy`** to perform **static analysis**. `mypy` is the **static type checker** that runs *before* execution and flags the ambiguity in `do_it_typed` (returning `int` sometimes and `dict` other times). This forces the developer to refactor the logic for clarity.

-----

## Tool 2: Linting, Formatting, and Docstrings (Fixing Readability)

Once the code is logically correct, we make it beautiful and easy to read.

### **Linting and Formatting with Ruff**

**Ruff** is an extremely fast tool that combines both linting (checking for programmatic errors) and formatting (enforcing style). It ensures all code is consistently spaced and follows best practices.

**Running Ruff**

1.  We run `ruff format .` on the entire project. This instantly fixes indentation, line length, and spacing issues.
2.  We run `ruff check .` to enforce things like Python's naming conventions and complexity rules.

This process is typically automated using a **pre-commit hook**, ensuring that bad style or format never even makes it into the version control history.

### **Docstrings**

A **docstring** explains what the code does, why it does it, and what inputs/outputs are involved.

**Standardized Docstrings**

1.  We will use the **VS Code extension `njpwerner.autodocstring`** to quickly generate a template.

2.  We'll adopt the **Google Style** because it's highly readable and uses clear `Args:`, `Returns:`, and `Raises:` sections.

    ```python linenums="1"
    def calculate_compound_interest(principal: float, rate: float, time: int) -> float:
        """Calculates the compound interest over a period of time. (Google Style)

        Args:
            principal (float): The initial amount of money (P).
            rate (float): The annual interest rate (r), as a decimal.
            time (int): The number of years (t).

        Returns:
            float: The total amount accrued (A).
        """
        return principal * (1 + rate) ** time
    ```

-----

## Tool 3: Pydantic (Fixing Fragile Data Structures)

**Pydantic** is the solution to **Code Smell 2** (Unstructured Data). It forces dictionary-like data to conform to an object-oriented structure, eliminating runtime errors caused by missing keys or wrong types.

### **Building Robust Data Models**

We will refactor the `process(data)` function by defining its input structure as a **Pydantic `BaseModel`**.

**Basic Model Definition:**We define the expected input using type hints. Pydantic validates and coerces the data upon instantiation.

```python linenums="1"
from pydantic import BaseModel, ValidationError
from typing import List, Optional

# The model defines the structure for the input data
class User(BaseModel):
    age: int
    status: UserStatus # Using our custom Enum

# Refactored function: Input is now a robust User object, not a fragile dict.
def process_user(user: User):
    if user.age > 18 and user.status == UserStatus.ACTIVE:
        return {"ok": True, "msg": "allowed"}
    return {"ok": False}
```

### **Complex Models (Inheritance & Composition):** 

We use OOP principles to define complex data structures, which are then used as type hints.

* **Inheritance:** We extend a base model to add specific fields.
* **Composition:** A model "has a" list of other models.

<!-- end list -->

```python linenums="1"
from datetime import date
from pydantic import BaseModel, Field

# Inheritance: TeamMember is a special type of User
class TeamMember(User):
    team_id: str
    is_lead: bool = False # Field with a default value

# Composition: Project model "has a" list of TeamMember objects
class Project(BaseModel):
    name: str = Field()
    members: List[TeamMember]
    date: Optional[date] = None  # Optional field
    budget: Optional[float] = Field(default=None, ge=0, le=999_999_999.0) 

# When we create a Project, Pydantic validates ALL nested models automatically!
project_data = {
    "name": "Apollo",
    "members": [
        {"age": 35, "status": "active", "team_id": "T101", "name": "Alice"},
        # The following would fail validation: missing 'age' will raise an error
        # {"status": "active", "team_id": "T102", "name": "Bob"}
    ],
    "date": date.today()
    "budget": 1_000_000.0
}

# Try to unpack the data into a Project
try:
    project = Project(**project_data)  # (1)!

except ValidationError as e:
    print(f"Validation Error: {e}")
```
{ .annotate }

1. Alternatively, we have other options.
    - We could use the `.parse_obj()` `classmethod`, like `Project.parse_obj(project_data)`.
    - Fill out the model directly:
        ```python

        project = Project(
            name="Apollo",
            members=[
                TeamMember(age=35, status="active", team_id="T101", name="Alice"),
                ...
            ],
            ...
        )

        ```
    <!-- end list -->

-----

## The "Good Code" Result

By applying these practices, the initial "code smells" are transformed into clear, reliable, and production-ready code:

| Old Code Smell | Applied Tools | New, Robust Code |
| :--- | :--- | :--- |
| **Code Smell 1** (Ambiguity) | Type Hints, Ruff, Docstrings | The types are clear, and the logic is broken into readable, single-purpose functions (which `ruff` encourages). The return type is always `int` for consistency. |
| **Code Smell 2** (Fragile Data) | Pydantic, Type Hints | The function input is a Pydantic object, eliminating runtime key errors. Logic is clean. |

```python title="Code Smell 1" linenums="1"
def do_it(x: int, y: int) -> int | dict[str, int]:
    """
    Computes a value based on x and y.
    If x is truthy, z = x + y; otherwise, z = y * 2.
    Returns a dictionary {"a": z} if z > 100, else returns z.

    Args:
        x (int): First integer input.
        y (int): Second integer input.

    Returns:
        int | dict[str, int]: Result based on computation.
    """
    z = x + y if x else y * 2
    if z > 100:
        return {"a": z}
    return z
```

!!! warning "Dictionaries or Pydantic?"
    As a personal preference, I usually default to Pydantic objects rather than working with dictionary types, however you don't have to chose only one. Sometimes you want the speed/comfort of the standard `dict()` or `set()`, but sometimes there is a benefit to have something with more defined structure.

```python title="Code Smell 2" linenums="1"
from enum import StrEnum
from pydantic import BaseModel

class AccessLevelsEnum(StrEnum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class UserStatusEnum(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class Permissions(BaseModel):
    level: AccessLevelsEnum = AccessLevelsEnum.MEMBER
    extra: str | None = None  # Some other random placeholder field

class InputData(BaseModel):
    age: int
    status: UserStatusEnum = UserStatusEnum.ACTIVE
    permissions: Permissions

class OutputData(BaseModel):
    ok: bool
    msg: str | None = None

def process(data: InputData) -> OutputData:
    """
    Checks if the user is allowed based on age and status.

    Args:
        data (InputData): Input data containing age, status, and extra permissions information.

    Returns:
        OutputData: Result indicating if allowed, with a message if allowed.
    """
    if (data.age > 18 and data.status == UserStatusEnum.ACTIVE) or (data.permissions.level == AccessLevelsEnum.ADMIN):
        return OutputData(ok=True, msg="allowed")
    return OutputData(ok=False)
```

!!! info "Class Structure"
    ```mermaid
    classDiagram
        class AccessLevelsEnum {
            ADMIN
            MEMBER
        }
        class UserStatusEnum {
            ACTIVE
            INACTIVE
            SUSPENDED
        }
        class Permissions {
            level: AccessLevelsEnum
            extra: str | None
        }
        class InputData {
            age: int
            status: UserStatusEnum
            permissions: Permissions
        }
        class OutputData {
            ok: bool
            msg: str | None
        }
        Permissions --> AccessLevelsEnum
        InputData --> UserStatusEnum
        InputData --> Permissions
    ```

-----

## Recommended Exercises & Homework

This week's homework is a comprehensive exercise that asks you to take a "bad code" example and apply all the professional practices we covered today.

**The Starting Code (Configuration Loader):**

Imagine you are given this script that loads a complex configuration dictionary for a hypothetical application:

```python title="app_config_loader.py" linenums="1"
def load_config(settings):
    # Very fragile access, no type checking, poor structure
    if settings.get("database").get("port") == 5432:
        conn_string = f"postgresql://{settings['database']['user']}@{settings['database']['host']}"
        print("Using PostgreSQL default port.")
    else:
        conn_string = "invalid"

    if settings.get("environment") == "dev":
        is_debug = True
    else:
        is_debug = False

    return {"connection": conn_string, "debug": is_debug}
```

**Your Tasks (Refactor and Validate):**

1. Code Organization & Readability:
    - Install ruff into your choice of development environment (preferably devcontainer).
    - Run `ruff format` and `ruff check` on the script. Address and fix any errors it reports.
    - Write clear, standardized docstrings (e.g., Google Style) for all functions and methods.
2. Type Constraint Implementation:
    - Create a custom `StrEnum` for the environment setting (e.g., `Environment.DEV`, `Environment.PROD`).
    - Create a `Literal` type to constrain the allowed database type (e.g., `"postgresql"`, `"mysql"`).
3. Pydantic Validation (Complex Structures):
    - Define a `BaseModel` called `DBConfig` that uses the appropriate type hints for host, port, user, type (using your `Literal`), and password.
    - Define a final model, `AppConfig`, that uses composition to include the `DBConfig` model and includes its own field for `environment` (using your custom `StrEnum`).
    - Modify `load_config` to accept and return your `AppConfig` Pydantic model, ensuring that the function will now robustly validate any input data automatically.

!!! example "Challenge: Auto-computed Fields"
    Try to include a new auto calculated field to `AppConfig` called `conn_string`, which is the combination of all the fields needed to reconstruct the string `f"postgresql://{settings['database']['user']}@{settings['database']['host']}"`.

This exercise will give you hands-on experience in making a codebase robust and production-ready.

### Suggested Readings & Resources

- **Ruff Documentation:** [Getting Started with Ruff](https://docs.astral.sh/ruff/tutorial/) - Learn how to set up and configure this powerful linter/formatter.
- **Pydantic Documentation:** [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/) - Explore the "Defining models" and "Validation" sections.
- **Real Python:** [Python Docstrings Guide](https://realpython.com/documenting-python-code/) - Excellent resource showing different docstring styles.
- **Python `typing`:** [PEP 586 (Literal Types)](https://peps.python.org/pep-0586/) and [PEP 647 (Type Guards)](https://peps.python.org/pep-0647/) - Deepen your understanding of specific type hints.
