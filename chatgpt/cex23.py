"""
This module contains examples of overly complex nested conditionals that should be flagged by SonarQube.
Deeply nested conditionals make code hard to understand, test, and maintain.
"""

from enum import Enum
from typing import Dict, Any, List


# ISSUE: Deeply nested conditionals for user permissions
def check_user_permission_nested(user: Dict[str, Any], resource: Dict[str, Any], action: str) -> bool:
    """
    Check if a user has permission to perform an action on a resource.
    Contains deeply nested conditionals that make the logic hard to follow.
    """
    if user is not None:
        if "role" in user:
            if user["role"] == "admin":
                # Admins can do anything
                return True
            elif user["role"] == "manager":
                if resource is not None:
                    if "type" in resource:
                        if resource["type"] == "document":
                            if action in ["read", "write", "update"]:
                                if "department" in user and "department" in resource:
                                    if user["department"] == resource["department"]:
                                        # Managers can read, write, and update documents in their department
                                        return True
                                    else:
                                        if action == "read":
                                            if "visibility" in resource:
                                                if resource["visibility"] == "public":
                                                    # Managers can read public documents from other departments
                                                    return True
                                                else:
                                                    return False
                                            else:
                                                return False
                                        else:
                                            return False
                                else:
                                    return False
                            elif action == "delete":
                                if "created_by" in resource:
                                    if resource["created_by"] == user["id"]:
                                        # Managers can delete documents they created
                                        return True
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        elif resource["type"] == "report":
                            if action in ["read", "generate"]:
                                # Managers can read and generate reports
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            elif user["role"] == "employee":
                if resource is not None:
                    if "type" in resource:
                        if resource["type"] == "document":
                            if action == "read":
                                if "visibility" in resource:
                                    if resource["visibility"] == "public":
                                        # Employees can read public documents
                                        return True
                                    elif resource["visibility"] == "internal":
                                        if "department" in user and "department" in resource:
                                            if user["department"] == resource["department"]:
                                                # Employees can read internal documents in their department
                                                return True
                                            else:
                                                return False
                                        else:
                                            return False
                                    else:
                                        return False
                                else:
                                    return False
                            elif action in ["write", "update"]:
                                if "created_by" in resource:
                                    if resource["created_by"] == user["id"]:
                                        # Employees can write and update documents they created
                                        return True
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        elif resource["type"] == "report":
                            if action == "read":
                                if "department" in user and "department" in resource:
                                    if user["department"] == resource["department"]:
                                        # Employees can read reports in their department
                                        return True
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False
