## ADDED Requirements

### Requirement: Achievements tab in Mini App
The Mini App SHALL display an "Ачивки" tab in the tab bar alongside existing tabs. The tab SHALL be accessible at all times.

#### Scenario: Tab is visible and selectable
- **WHEN** the Mini App loads
- **THEN** a tab labeled "🏆 Ачивки" SHALL appear in the tab bar after entity type tabs

### Requirement: Two achievement progress chains displayed
The Achievements tab SHALL display two separate horizontal progress-chain trees: one for each entity type (girl, beautiful_girl). Each tree SHALL have a section header with the entity type display name.

#### Scenario: Both trees rendered on the tab
- **WHEN** the user navigates to the Achievements tab
- **THEN** two progress chains SHALL be displayed vertically, one for "Девочка" and one for "Красивая девочка"

### Requirement: Progress chain visualization
Each achievement tree SHALL render as a horizontal chain of connected nodes. Each node SHALL display the achievement emoji, name, and threshold count. Nodes SHALL be connected by horizontal lines.

#### Scenario: Unlocked achievement node appearance
- **WHEN** the user has unlocked an achievement
- **THEN** the node SHALL be displayed with a green background/border indicating completion

#### Scenario: Locked achievement node appearance
- **WHEN** the user has NOT unlocked an achievement
- **THEN** the node SHALL be displayed with a gray background/border indicating it is locked

### Requirement: Default view shows current user
The Achievements tab SHALL display the current Telegram user's achievement progress by default when first navigated to.

#### Scenario: Initial load shows own achievements
- **WHEN** the user opens the Achievements tab for the first time
- **THEN** the progress chains SHALL reflect the current user's unlocked achievements

### Requirement: User selection dropdown
The Achievements tab SHALL include a dropdown (select) control populated with all users. Selecting a different user SHALL reload the achievement progress for that user.

#### Scenario: Viewing another user's achievements
- **WHEN** the user selects a different user from the dropdown
- **THEN** the progress chains SHALL update to show the selected user's unlocked achievements

#### Scenario: Dropdown defaults to current user
- **WHEN** the Achievements tab loads
- **THEN** the dropdown SHALL show the current user as the selected value
