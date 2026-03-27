## MODIFIED Requirements

### Requirement: Entry creation with achievement check
After creating an entry via `/add_girl` or `/add_beautiful_girl` commands, the bot handler SHALL check for newly unlocked achievements and send congratulation messages for each. This applies to both the "skip contact" and "provide contact" flows.

#### Scenario: Entry with contact triggers achievement check
- **WHEN** a user provides a contact username and the entry is created
- **THEN** the handler SHALL call the achievement check service and send achievement messages before the final confirmation

#### Scenario: Entry without contact triggers achievement check
- **WHEN** a user skips the contact and the entry is created
- **THEN** the handler SHALL call the achievement check service and send achievement messages before the final confirmation
