#!/usr/bin/env python3
"""
🎓 Student Profile Setup Wizard
Interactive configuration tool for the Assignment Master Vault.
Prompts for user academic credentials and stores them locally in `student_profile.json`.
"""

import os
import sys
import json
import argparse
from pathlib import Path

PROFILE_FILENAME = "student_profile.json"
TEMPLATE_FILENAME = "student_profile.template.json"

VAULT_DIR = Path(__file__).resolve().parent
PROFILE_PATH = VAULT_DIR / PROFILE_FILENAME
TEMPLATE_PATH = VAULT_DIR / TEMPLATE_FILENAME


def get_profile():
    """Returns the configured profile dict, or None if not configured."""
    if PROFILE_PATH.exists():
        try:
            with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Warning: Could not read {PROFILE_FILENAME}: {e}")
            return None
    return None


def prompt_field(label, default=""):
    """Prompts the user for a field with an optional default."""
    if default:
        prompt_text = f"  👉 {label} [{default}]: "
    else:
        prompt_text = f"  👉 {label}: "
    
    val = input(prompt_text).strip()
    return val if val else default


def interactive_setup(force=False):
    """Runs the interactive wizard to configure student credentials."""
    existing = get_profile() or {}
    if existing and not force:
        print("\n" + "=" * 60)
        print("ℹ️ Existing Student Profile Detected:")
        print("=" * 60)
        for k, v in existing.items():
            print(f"  • {k.replace('_', ' ').title()}: {v}")
        print("-" * 60)
        reconf = input("Do you want to reconfigure your profile? (y/N): ").strip().lower()
        if reconf not in ("y", "yes"):
            print("Keeping existing profile. Setup complete!\n")
            return existing

    print("\n" + "=" * 65)
    print("🎓 ASSIGNMENT MASTER VAULT — STUDENT PROFILE SETUP")
    print("=" * 65)
    print("Please enter your academic credentials.")
    print("These will be used to automatically format title pages and headers")
    print("matching your university standards without manual edits.\n")

    name = ""
    while not name:
        name = prompt_field("Full Student Name", existing.get("student_name", ""))
        if not name:
            print("     [!] Student name is required.")

    student_id = ""
    while not student_id:
        student_id = prompt_field("Registration / Student ID Number", existing.get("student_id", ""))
        if not student_id:
            print("     [!] Registration ID is required.")

    institution = prompt_field("University / Institution Name", existing.get("institution_name", "My University"))
    campus = prompt_field("Campus Name / City", existing.get("campus_name", "Main Campus"))
    campus_code = prompt_field("Campus / Short Code (e.g., UNIV-MAIN)", existing.get("campus_code", "UNIV-01"))
    degree = prompt_field("Degree Program (e.g., BS Computer Science)", existing.get("degree_program", "BS Computer Science"))
    standing = prompt_field("Current Standing / Semester (e.g., 6th Semester)", existing.get("current_standing", "6th Semester"))
    section = prompt_field("Class Section / Cohort (e.g., Section A)", existing.get("class_section", "Section A"))
    department = prompt_field("Department / Faculty", existing.get("department", "Department of Computer Science"))
    output_dir = prompt_field("Default Output Folder", existing.get("output_dir", "./output"))

    profile = {
        "student_name": name,
        "student_id": student_id,
        "institution_name": institution,
        "campus_name": campus,
        "campus_code": campus_code,
        "degree_program": degree,
        "current_standing": standing,
        "class_section": section,
        "department": department,
        "output_dir": output_dir
    }

    try:
        with open(PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)
        print("\n" + "=" * 65)
        print(f"✅ Success! Profile saved to: {PROFILE_FILENAME}")
        print("🔒 Note: This file is ignored by git and stays private on your machine.")
        print("=" * 65 + "\n")
    except Exception as e:
        print(f"\n❌ Error saving profile: {e}")
        sys.exit(1)

    return profile


def ensure_profile():
    """Ensures a profile exists; prompts if missing."""
    profile = get_profile()
    if not profile:
        print("\n⚠️ No student profile configured yet. Launching setup wizard...")
        profile = interactive_setup()
    return profile


def main():
    parser = argparse.ArgumentParser(description="Student Profile Setup Wizard for Assignment Master Vault")
    parser.add_argument("--check", action="store_true", help="Check if profile is configured")
    parser.add_argument("--print", dest="show", action="store_true", help="Display current profile")
    parser.add_argument("--reset", action="store_true", help="Force reconfiguring profile")
    args = parser.parse_args()

    if args.check:
        profile = get_profile()
        if profile and profile.get("student_name"):
            print(f"Profile configured for: {profile.get('student_name')} ({profile.get('student_id')})")
            sys.exit(0)
        else:
            print("No profile found.")
            sys.exit(1)

    if args.show:
        profile = get_profile()
        if profile:
            print(json.dumps(profile, indent=2))
        else:
            print("No profile configured yet. Run without arguments to set up.")
        return

    interactive_setup(force=args.reset)


if __name__ == "__main__":
    main()
